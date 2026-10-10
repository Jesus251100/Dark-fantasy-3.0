# Verifica que Postgres, el API y el juego esten listos antes de iniciar sesion.
$ErrorActionPreference = "Continue"

function Ok($msg) { Write-Host "  OK   $msg" -ForegroundColor Green }
function Fail($msg) { Write-Host "  FAIL $msg" -ForegroundColor Red }

Write-Host ""
Write-Host "Dark Fantasy - chequeo previo" -ForegroundColor Cyan
Write-Host ""

$pg = $false
try {
  $running = docker inspect -f "{{.State.Running}}" darkfantasy-pg 2>$null
  if ($running -eq "true") { Ok "PostgreSQL (Docker darkfantasy-pg, puerto 5433)"; $pg = $true }
  else { Fail "PostgreSQL apagado. Corre: docker start darkfantasy-pg" }
} catch {
  Fail "Docker no responde. Abre Docker Desktop."
}

$api = $false
try {
  $salud = Invoke-RestMethod -Uri "http://127.0.0.1:3001/api/salud" -TimeoutSec 4
  if ($salud.ok) { Ok "API backend  http://127.0.0.1:3001  ($($salud.baseDatos))"; $api = $true }
  else { Fail "API respondio mal: $($salud.error)" }
} catch {
  Fail "API apagada. En otra terminal: cd backend ; npm run dev"
}

$front = $false
try {
  $code = (Invoke-WebRequest -Uri "http://127.0.0.1:5173/" -UseBasicParsing -TimeoutSec 4).StatusCode
  if ($code -eq 200) { Ok "Juego Vue   http://127.0.0.1:5173"; $front = $true }
  else { Fail "El juego respondio $code" }
} catch {
  Fail "Juego apagado. En otra terminal: npm run dev"
}

$login = $false
if ($api) {
  try {
    $body = '{"correo":"jugador@darkfantasy.local","clave":"jugador123","rol":"jugador"}'
    $r = Invoke-RestMethod -Uri "http://127.0.0.1:3001/api/auth/login" -Method POST -ContentType "application/json" -Body $body -TimeoutSec 6
    if ($r.token) { Ok "Login de prueba (jugador@darkfantasy.local)"; $login = $true }
    else { Fail "Login no devolvio token" }
  } catch {
    Fail "Login fallo. Revisa correo/clave o la base de datos."
  }
} else {
  Fail "Login no se probo (API apagada)"
}

Write-Host ""
if ($pg -and $api -and $front -and $login) {
  Write-Host "Todo listo. Abre http://127.0.0.1:5173/login" -ForegroundColor Green
} else {
  Write-Host "Falta algo. Enciende lo que salio FAIL y corre otra vez verificar.ps1" -ForegroundColor Yellow
}
Write-Host ""
