from pathlib import Path

p = Path(r"C:\Users\sanch\Downloads\Dark-fantasy-3.0\src\views\UsersView.vue")
t = p.read_text(encoding="utf-8")
start = t.index("<script setup lang=\"ts\">")
end = t.index("</script>")
script = r'''<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import AppSidebar from '@/components/AppSidebar.vue'
import { api } from '@/api/cliente'
import avMessi from '@/assets/img/avatars/user-messironaldo107.png'
import avMimami from '@/assets/img/avatars/user-mimami456.png'
import avDonpollo from '@/assets/img/avatars/user-donpollo67.png'
import avNoob from '@/assets/img/avatars/user-noobmaster69.png'
import avDavo from '@/assets/img/avatars/user-davoxeneixe.png'
import avJhonb from '@/assets/img/avatars/user-jhonblacked.png'
import avHomla from '@/assets/img/avatars/user-homladereff.png'
import avEso from '@/assets/img/avatars/user-esotilnxd.png'
import avArenis from '@/assets/img/avatars/user-jhon-arenis.png'

const AVATARES = [avMessi, avMimami, avDonpollo, avNoob, avDavo, avJhonb, avHomla, avEso, avArenis]

type User = {
  id: string
  name: string
  username: string
  level: number
  coins: number
  gems: number
  countryFlag: string
  status: 'Conectado' | 'Desconectado'
  avatar: string
  xp: number
  xpPercent: number
  matches: string
  wins: string
  winRate: number
  joined: string
  lastOnline: string
}

const query = ref('')
const selectedId = ref('')
const users = ref<User[]>([])

onMounted(async () => {
  try {
    const data = await api<{
      usuarios: {
        id: string
        correo: string
        nombre: string
        rol: string
        creadoEn: string
        coins: number
        diamonds: number
        wins: number
        highestUnlocked: number
        completed?: number[]
        partidas: number
      }[]
    }>('/api/admin/usuarios')
    users.value = data.usuarios.map((u, i) => {
      const completed = u.completed?.length ?? 0
      const matches = u.partidas ?? 0
      const wins = u.wins ?? 0
      return {
        id: u.id,
        name: u.nombre,
        username: u.correo,
        level: Math.max(1, completed),
        coins: u.coins,
        gems: u.diamonds,
        countryFlag: u.rol === 'administrador' ? '🛡️' : '🎮',
        status: 'Conectado',
        avatar: AVATARES[i % AVATARES.length] ?? avMessi,
        xp: completed * 100,
        xpPercent: Math.round((completed / 10) * 100),
        matches: String(matches),
        wins: String(wins),
        winRate: matches > 0 ? Math.round((wins / matches) * 100) : 0,
        joined: new Date(u.creadoEn).toLocaleDateString('es-CO'),
        lastOnline: u.rol,
      }
    })
    if (users.value[0]) selectedId.value = users.value[0].id
  } catch {
    users.value = []
  }
})

const filteredUsers = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return users.value
  return users.value.filter(
    (u) => u.name.toLowerCase().includes(q) || u.username.toLowerCase().includes(q),
  )
})

const selected = computed(() => users.value.find((u) => u.id === selectedId.value) ?? users.value[0])
</script>'''
p.write_text(t[:start] + script + t[end + len("</script>") :], encoding="utf-8")
print("patched", p.stat().st_size)
