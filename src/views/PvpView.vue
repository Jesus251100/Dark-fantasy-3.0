<script setup lang="ts">
import { onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api/cliente'

type Modo = 'mismo-nivel' | 'duelo'
type Jugador = { id: string; nombre: string }
type Sala = { id: string; codigo: string; modo: Modo; nivel: number; estado: 'esperando' | 'lista'; jugadores: Jugador[]; soyAnfitrion: boolean }

const router = useRouter()
const modo = ref<Modo>('mismo-nivel')
const nivel = ref(1)
const codigo = ref('')
const sala = ref<Sala | null>(null)
const mensaje = ref('')
const cargando = ref(false)
let poll: ReturnType<typeof setInterval> | null = null

function detenerPoll() {
  if (poll) clearInterval(poll)
  poll = null
}
async function crear(tipo: 'buscar' | 'invitacion') {
  mensaje.value = ''
  cargando.value = true
  try {
    const data = await api<{ sala: Sala; emparejado?: boolean }>(`/api/pvp/${tipo}`, {
      method: 'POST', body: JSON.stringify({ modo: modo.value, nivel: nivel.value }),
    })
    sala.value = data.sala
    mensaje.value = tipo === 'buscar'
      ? (data.emparejado ? '¡Contrincante encontrado!' : 'Buscando rival… comparte el código para invitar a alguien.')
      : 'Sala creada. Comparte el código con tu amigo.'
    if (sala.value.estado === 'esperando') poll = setInterval(actualizar, 2500)
  } catch (e) {
    mensaje.value = e instanceof Error ? e.message : 'No se pudo crear la sala.'
  } finally { cargando.value = false }
}
async function actualizar() {
  if (!sala.value) return
  try {
    const data = await api<{ sala: Sala }>(`/api/pvp/${sala.value.id}`)
    sala.value = data.sala
    if (sala.value.estado === 'lista') {
      detenerPoll()
      mensaje.value = '¡Los dos jugadores están listos! El siguiente paso es iniciar la partida.'
    }
  } catch (e) {
    detenerPoll()
    mensaje.value = e instanceof Error ? e.message : 'No se pudo consultar la sala.'
  }
}
async function unirse() {
  mensaje.value = ''
  cargando.value = true
  try {
    const data = await api<{ sala: Sala }>('/api/pvp/unirse', {
      method: 'POST', body: JSON.stringify({ codigo: codigo.value.trim() }),
    })
    sala.value = data.sala
    mensaje.value = '¡Te has unido a la sala!'
  } catch (e) {
    mensaje.value = e instanceof Error ? e.message : 'No se pudo entrar.'
  } finally { cargando.value = false }
}
async function salir() {
  detenerPoll()
  if (sala.value) {
    try { await api(`/api/pvp/${sala.value.id}/salir`, { method: 'POST' }) } catch { /* la sala puede haber expirado */ }
  }
  sala.value = null
  mensaje.value = 'Has salido de la sala.'
}
onUnmounted(detenerPoll)
</script>

<template>
  <main class="pvp-page">
    <section class="pvp-panel">
      <button class="back" @click="router.push('/lobby')">← Volver al lobby</button>
      <h1>⚔ JUGADOR CONTRA JUGADOR</h1>
      <p class="intro">Enfréntate a otro jugador en una sala privada de dos participantes.</p>

      <template v-if="!sala">
        <label>Modalidad</label>
        <div class="choices">
          <button :class="{ selected: modo === 'mismo-nivel' }" @click="modo = 'mismo-nivel'">
            <strong>Mismo nivel</strong><small>Mismo desafío y configuración para ambos</small>
          </button>
          <button :class="{ selected: modo === 'duelo' }" @click="modo = 'duelo'">
            <strong>Duelo</strong><small>Enfrentamiento directo 1 contra 1</small>
          </button>
        </div>
        <label for="nivel">Nivel del desafío</label>
        <select id="nivel" v-model.number="nivel">
          <option v-for="n in 10" :key="n" :value="n">Nivel {{ n }}</option>
        </select>
        <button class="primary" :disabled="cargando" @click="crear('buscar')">BUSCAR RIVAL ALEATORIO</button>
        <button class="secondary" :disabled="cargando" @click="crear('invitacion')">CREAR SALA PARA INVITAR</button>
        <div class="join">
          <label for="codigo">¿Tienes un código de invitación?</label>
          <div class="join-row">
            <input id="codigo" v-model="codigo" maxlength="6" inputmode="numeric" placeholder="Código de 6 dígitos" />
            <button :disabled="cargando || codigo.trim().length !== 6" @click="unirse">UNIRME</button>
          </div>
        </div>
      </template>

      <template v-else>
        <div class="room-code">
          <small>CÓDIGO DE SALA</small><strong>{{ sala.codigo }}</strong>
          <button @click="navigator.clipboard?.writeText(sala.codigo)">COPIAR CÓDIGO</button>
        </div>
        <p class="status">{{ sala.estado === 'lista' ? 'Sala completa' : 'Esperando al segundo jugador…' }}</p>
        <ul class="players"><li v-for="(jugador, i) in sala.jugadores" :key="jugador.id">⚔ {{ jugador.nombre }} <span>{{ i === 0 ? 'Anfitrión' : 'Contrincante' }}</span></li></ul>
        <p v-if="sala.estado === 'lista'" class="notice">Emparejamiento completado. La sincronización de la partida en tiempo real es la siguiente etapa de implementación.</p>
        <button class="secondary" @click="salir">SALIR DE LA SALA</button>
      </template>
      <p v-if="mensaje" class="message" role="status">{{ mensaje }}</p>
    </section>
  </main>
</template>

<style scoped>
.pvp-page{min-height:100vh;display:grid;place-items:center;padding:24px;box-sizing:border-box;background:radial-gradient(ellipse at center,#182b45,#080d18 75%);color:#eee;font-family:Georgia,serif}
.pvp-panel{width:min(620px,100%);box-sizing:border-box;padding:30px;border:1px solid #b89b52;border-radius:16px;background:#101a2bea;box-shadow:0 0 32px #0009}
h1{text-align:center;color:#e8c86a;font-size:clamp(1.3rem,4vw,2rem)}.intro{text-align:center;color:#c5cbd5;margin-bottom:28px}
.back{background:none;border:0;color:#8bdcff;cursor:pointer;font-size:1rem}
label{display:block;margin:18px 0 8px;color:#e8d7a2}.choices{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.choices button,.secondary,.primary,.join-row button{border:1px solid #52647c;border-radius:10px;padding:14px;background:#172b48;color:#fff;cursor:pointer}
.choices button{display:flex;flex-direction:column;gap:8px;text-align:left}.choices .selected{border-color:#e8c86a;box-shadow:0 0 12px #e8c86a55}
small{color:#b9c6d6}.choices small{font-size:.8rem}select,input{width:100%;box-sizing:border-box;padding:12px;border-radius:8px;border:1px solid #64748b;background:#0b1422;color:white}
.primary,.secondary{width:100%;margin-top:14px;font-weight:bold;letter-spacing:.5px}.primary{background:#244c78;border-color:#66bce7}.secondary{background:#332b22;border-color:#b89b52}
button:disabled{opacity:.5;cursor:not-allowed}.join{margin-top:26px;padding-top:18px;border-top:1px solid #52647c}.join-row{display:flex;gap:8px}.join-row button{white-space:nowrap}
.room-code{text-align:center;padding:22px;margin:24px 0;background:#0a1321;border:1px dashed #c6a755;border-radius:12px;display:grid;gap:10px}.room-code strong{font-size:2.4rem;letter-spacing:8px;color:#f2d77f}.room-code button{justify-self:center;background:none;color:#8bdcff;border:0;cursor:pointer}
.status,.message{text-align:center;color:#f1d47b}.players{list-style:none;padding:0}.players li{padding:14px;border-bottom:1px solid #52647c}.players span{float:right;color:#9caec2}.notice{padding:12px;background:#25364b;border-radius:8px;color:#d9e6f5;font-size:.9rem}
@media(max-width:480px){.pvp-panel{padding:20px}.choices{grid-template-columns:1fr}.join-row{flex-direction:column}}
</style>
