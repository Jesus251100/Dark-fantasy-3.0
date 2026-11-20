import { randomInt, randomUUID } from 'node:crypto'
import { Router } from 'express'
import { z } from 'zod'
import { authObligatoria } from './auth'

type ModoPvp = 'mismo-nivel' | 'duelo'
type EstadoSala = 'esperando' | 'lista'
type Jugador = { id: string; nombre: string }
type Sala = {
  id: string
  codigo: string
  modo: ModoPvp
  nivel: number
  estado: EstadoSala
  jugadores: Jugador[]
  creadaEn: number
}

const router = Router()
router.use(authObligatoria)

// MVP: salas en memoria. Para producción se debe mover a PostgreSQL/Redis
// y usar WebSocket para sincronización de la partida.
const salas = new Map<string, Sala>()
const LIMITE_SALA_MS = 30 * 60 * 1000

function limpiarSalas() {
  const ahora = Date.now()
  for (const [id, sala] of salas) {
    if (ahora - sala.creadaEn > LIMITE_SALA_MS) salas.delete(id)
  }
}

function vista(sala: Sala, usuarioId: string) {
  return {
    id: sala.id,
    codigo: sala.codigo,
    modo: sala.modo,
    nivel: sala.nivel,
    estado: sala.estado,
    jugadores: sala.jugadores,
    soyAnfitrion: sala.jugadores[0]?.id === usuarioId,
  }
}

function nuevaSala(usuario: Jugador, modo: ModoPvp, nivel: number): Sala {
  let codigo = ''
  do {
    codigo = randomInt(100000, 999999).toString()
  } while ([...salas.values()].some((s) => s.codigo === codigo && s.estado === 'esperando'))

  const sala: Sala = {
    id: randomUUID(),
    codigo,
    modo,
    nivel,
    estado: 'esperando',
    jugadores: [usuario],
    creadaEn: Date.now(),
  }
  salas.set(sala.id, sala)
  return sala
}

router.post('/buscar', (req, res) => {
  limpiarSalas()
  const parsed = z.object({
    modo: z.enum(['mismo-nivel', 'duelo']),
    nivel: z.number().int().min(1).max(10).default(1),
  }).safeParse(req.body)
  if (!parsed.success) {
    res.status(400).json({ error: 'Modo o nivel inválido.' })
    return
  }

  const jugador = { id: req.usuario!.sub, nombre: req.usuario!.nombre }
  const existente = [...salas.values()].find((s) =>
    s.estado === 'esperando' &&
    s.modo === parsed.data.modo &&
    s.nivel === parsed.data.nivel &&
    s.jugadores.length === 1 &&
    s.jugadores[0]?.id !== jugador.id,
  )

  if (existente) {
    existente.jugadores.push(jugador)
    existente.estado = 'lista'
    res.json({ sala: vista(existente, jugador.id), emparejado: true })
    return
  }

  const sala = nuevaSala(jugador, parsed.data.modo, parsed.data.nivel)
  res.status(201).json({ sala: vista(sala, jugador.id), emparejado: false })
})

router.post('/invitacion', (req, res) => {
  limpiarSalas()
  const parsed = z.object({
    modo: z.enum(['mismo-nivel', 'duelo']),
    nivel: z.number().int().min(1).max(10).default(1),
  }).safeParse(req.body)
  if (!parsed.success) {
    res.status(400).json({ error: 'Modo o nivel inválido.' })
    return
  }
  const sala = nuevaSala(
    { id: req.usuario!.sub, nombre: req.usuario!.nombre },
    parsed.data.modo,
    parsed.data.nivel,
  )
  res.status(201).json({ sala: vista(sala, req.usuario!.sub) })
})

router.post('/unirse', (req, res) => {
  limpiarSalas()
  const parsed = z.object({ codigo: z.string().regex(/^\d{6}$/) }).safeParse(req.body)
  if (!parsed.success) {
    res.status(400).json({ error: 'El código debe tener 6 números.' })
    return
  }
  const sala = [...salas.values()].find((s) => s.codigo === parsed.data.codigo)
  if (!sala) {
    res.status(404).json({ error: 'No existe una sala con ese código.' })
    return
  }
  if (sala.estado !== 'esperando' || sala.jugadores.length >= 2) {
    res.status(409).json({ error: 'La sala ya está completa.' })
    return
  }
  if (sala.jugadores.some((j) => j.id === req.usuario!.sub)) {
    res.json({ sala: vista(sala, req.usuario!.sub) })
    return
  }
  sala.jugadores.push({ id: req.usuario!.sub, nombre: req.usuario!.nombre })
  sala.estado = 'lista'
  res.json({ sala: vista(sala, req.usuario!.sub) })
})

router.get('/:id', (req, res) => {
  limpiarSalas()
  const sala = salas.get(req.params.id)
  if (!sala || !sala.jugadores.some((j) => j.id === req.usuario!.sub)) {
    res.status(404).json({ error: 'Sala no encontrada.' })
    return
  }
  res.json({ sala: vista(sala, req.usuario!.sub) })
})

router.post('/:id/salir', (req, res) => {
  const sala = salas.get(req.params.id)
  if (!sala || !sala.jugadores.some((j) => j.id === req.usuario!.sub)) {
    res.status(404).json({ error: 'Sala no encontrada.' })
    return
  }
  salas.delete(sala.id)
  res.json({ ok: true })
})

export default router
