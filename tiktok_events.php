<?php
/**
 * tiktok_events.php - Buffer Circolare e Bridge API per TikTok LIVE
 * Riceve eventi dal demone Python (es. server Contabo/VPS) e li serve al gioco tiktok.html via HTTPS (zero CORS).
 *
 * NOTE FOR OPEN-SOURCE / AI DEVELOPERS:
 * Imposta la variabile d'ambiente ANDROBS_BRIDGE_TOKEN nel tuo server web
 * oppure definisci una chiave segreta univoca condivisa con bridge.py.
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Bridge-Token');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// Token di autenticazione sicuro tra demone Python e backend web
$secret_token = getenv('ANDROBS_BRIDGE_TOKEN') ?: 'YOUR_SECURE_BRIDGE_TOKEN_HERE';

// Chiave opzionale per autorizzare il cambio di streamer target via GET
// (?target=NOME&key=CHIAVE). Se non impostata, il cambio resta aperto come
// prima; se impostata, chiunque indovini l'endpoint non può più dirottare
// la stanza monitorata dal bridge in mezzo alla live.
$panel_key = getenv('ANDROBS_PANEL_KEY') ?: '';

$data_dir = __DIR__ . '/tiktok_data';
if (!is_dir($data_dir)) {
    @mkdir($data_dir, 0755, true);
}

$queue_file = $data_dir . '/tiktok_live_queue.json';
$target_file = $data_dir . '/tiktok_target_user.json';
// Registro vincitori del torneo: chi ha già vinto non può vincere di
// nuovo (anti-ripetizione del premio e anti-farm da script).
$winners_file = $data_dir . '/tiktok_winners.json';

// Inizializza file se inesistenti
if (!file_exists($queue_file)) {
    file_put_contents($queue_file, json_encode([
        'last_id' => 0,
        'events' => []
    ], JSON_PRETTY_PRINT));
}
if (!file_exists($target_file)) {
    file_put_contents($target_file, json_encode([
        'user' => 'androbs_official',
        'updated_at' => time()
    ], JSON_PRETTY_PRINT));
}
if (!file_exists($winners_file)) {
    file_put_contents($winners_file, json_encode([], JSON_PRETTY_PRINT));
}

// -----------------------------------------------------------------------------
// POST: Ricezione eventi o cambio target dallo script bridge
// -----------------------------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw_input = file_get_contents('php://input');
    $payload = json_decode($raw_input, true);

    // Incoronazione vincitore: arriva dal BROWSER dello streamer (non dal
    // bridge, che qui non c'entra), quindi si autorizza con la chiave
    // pannello invece che col token del bridge.
    if (($payload['action'] ?? '') === 'crown') {
        if ($panel_key === '' || ($payload['key'] ?? '') !== $panel_key) {
            http_response_code(403);
            echo json_encode(['status' => 'error', 'message' => 'Chiave pannello mancante o errata']);
            exit;
        }
        $w_user = preg_replace('/[^a-zA-Z0-9_\.]/', '', str_replace('@', '', $payload['user'] ?? ''));
        $w_prize = htmlspecialchars(substr($payload['prize'] ?? '', 0, 40), ENT_QUOTES, 'UTF-8');
        if ($w_user === '') {
            http_response_code(400);
            echo json_encode(['status' => 'error', 'message' => 'Username non valido']);
            exit;
        }
        $winners = json_decode(@file_get_contents($winners_file), true) ?: [];
        $found = false;
        foreach ($winners as &$w) {
            if (strcasecmp($w['user'], $w_user) === 0) {
                $w['prize'] = $w_prize;
                $w['ts'] = time();
                $found = true;
                break;
            }
        }
        unset($w);
        if (!$found) {
            $winners[] = ['user' => $w_user, 'prize' => $w_prize, 'ts' => time()];
        }
        file_put_contents($winners_file, json_encode(array_values($winners), JSON_PRETTY_PRINT));
        echo json_encode(['status' => 'ok', 'winners' => count($winners)]);
        exit;
    }

    // Verifica Token di sicurezza
    $headers = getallheaders();
    $provided_token = $_SERVER['HTTP_X_BRIDGE_TOKEN'] ?? ($headers['X-Bridge-Token'] ?? ($payload['token'] ?? ''));
    if ($provided_token !== $secret_token) {
        http_response_code(403);
        echo json_encode(['status' => 'error', 'message' => 'Token non autorizzato']);
        exit;
    }

    $action = $payload['action'] ?? 'push_event';

    // 1. Aggiornamento target utente da monitorare
    if ($action === 'set_target' && !empty($payload['user'])) {
        $user = preg_replace('/[^a-zA-Z0-9_\.]/', '', str_replace('@', '', $payload['user']));
        file_put_contents($target_file, json_encode([
            'user' => $user,
            'updated_at' => time()
        ], JSON_PRETTY_PRINT));
        echo json_encode(['status' => 'ok', 'target_user' => $user]);
        exit;
    }

    // 2. Inserimento eventi reali nel buffer circolare
    $events_to_add = [];
    if (!empty($payload['events']) && is_array($payload['events'])) {
        $events_to_add = $payload['events'];
    } elseif (!empty($payload['type'])) {
        $events_to_add = [$payload];
    }

    if (!empty($events_to_add)) {
        $fp = fopen($queue_file, 'c+');
        if (flock($fp, LOCK_EX)) {
            $content = stream_get_contents($fp);
            $data = json_decode($content, true) ?: ['last_id' => 0, 'events' => []];

            foreach ($events_to_add as $ev) {
                $data['last_id']++;

                // Avatar: accetta solo URL http/https assoluti
                $avatar_url = '';
                $raw_avatar = $ev['avatar'] ?? '';
                if (is_string($raw_avatar) && filter_var($raw_avatar, FILTER_VALIDATE_URL)) {
                    $scheme = strtolower(parse_url($raw_avatar, PHP_URL_SCHEME) ?: '');
                    if ($scheme === 'http' || $scheme === 'https') {
                        $avatar_url = $raw_avatar;
                    }
                }

                $new_event = [
                    'id' => $data['last_id'],
                    'type' => $ev['type'] ?? 'join',
                    'user' => preg_replace('/[^a-zA-Z0-9_\.]/', '', str_replace('@', '', $ev['user'] ?? 'spettatore')),
                    'nickname' => htmlspecialchars(substr($ev['nickname'] ?? '', 0, 50), ENT_QUOTES, 'UTF-8'),
                    'avatar' => $avatar_url,
                    'text' => htmlspecialchars(substr($ev['text'] ?? '', 0, 100), ENT_QUOTES, 'UTF-8'),
                    'giftName' => htmlspecialchars($ev['giftName'] ?? '', ENT_QUOTES, 'UTF-8'),
                    'repeatCount' => (int)($ev['repeatCount'] ?? 1),
                    'giftValue' => max(0, (int)($ev['giftValue'] ?? 0)),
                    'timestamp' => time()
                ];
                $data['events'][] = $new_event;
            }

            // Mantieni solo gli ultimi 50 eventi (buffer circolare leggero in memoria)
            if (count($data['events']) > 50) {
                $data['events'] = array_slice($data['events'], -50);
            }

            ftruncate($fp, 0);
            rewind($fp);
            fwrite($fp, json_encode($data, JSON_PRETTY_PRINT));
            fflush($fp);
            flock($fp, LOCK_UN);
        }
        fclose($fp);
    }

    echo json_encode(['status' => 'ok', 'added' => count($events_to_add)]);
    exit;
}

// -----------------------------------------------------------------------------
// GET: Lettura eventi incrementali per tiktok.html o query target per bridge
// -----------------------------------------------------------------------------
$target_info = json_decode(@file_get_contents($target_file), true) ?: ['user' => 'androbs_official'];

// Se da browser viene passato ?target=USERNAME, aggiorna direttamente.
// Con ANDROBS_PANEL_KEY impostata richiede anche &key=CHIAVE per evitare che
// chiunque scopra l'endpoint possa dirottare la stanza monitorata.
if (!empty($_GET['target'])) {
    if ($panel_key !== '' && ($_GET['key'] ?? '') !== $panel_key) {
        http_response_code(403);
        echo json_encode(['status' => 'error', 'message' => 'Chiave pannello mancante o errata']);
        exit;
    }
    $user = preg_replace('/[^a-zA-Z0-9_\.]/', '', str_replace('@', '', $_GET['target']));
    if ($user === '') {
        http_response_code(400);
        echo json_encode(['status' => 'error', 'message' => 'Username non valido']);
        exit;
    }
    file_put_contents($target_file, json_encode([
        'user' => $user,
        'updated_at' => time()
    ], JSON_PRETTY_PRINT));
    $target_info['user'] = $user;
}

// Lista pubblica dei vincitori passati (l'overlay la legge per escludere
// chi ha già vinto dal prossimo premio).
if (isset($_GET['action']) && $_GET['action'] === 'winners') {
    $winners = json_decode(@file_get_contents($winners_file), true) ?: [];
    echo json_encode(['status' => 'ok', 'winners' => $winners]);
    exit;
}

// Se il daemon del bridge chiede solo l'account da monitorare
if (isset($_GET['action']) && $_GET['action'] === 'get_target') {
    echo json_encode([
        'status' => 'ok',
        'target_user' => $target_info['user'],
        'updated_at' => $target_info['updated_at'] ?? time()
    ]);
    exit;
}

// Lettura eventi incrementali ?since=ID
$since_id = isset($_GET['since']) ? (int)$_GET['since'] : 0;
$queue_data = json_decode(@file_get_contents($queue_file), true) ?: ['last_id' => 0, 'events' => []];

$new_events = [];
foreach ($queue_data['events'] as $ev) {
    if ($ev['id'] > $since_id) {
        $new_events[] = $ev;
    }
}

echo json_encode([
    'status' => 'ok',
    'last_id' => $queue_data['last_id'],
    'events' => $new_events,
    'target_user' => $target_info['user']
]);
