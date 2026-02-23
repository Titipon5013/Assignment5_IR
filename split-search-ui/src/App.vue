<template>
  <div class="min-h-screen bg-gradient-to-br from-black via-zinc-800 to-zinc-500 text-white font-sans selection:bg-zinc-600 selection:text-white">

    <div v-if="!hasSearched" class="flex flex-col items-center justify-center min-h-screen px-4">
      <h1 class="text-6xl md:text-8xl font-black mb-8 tracking-tighter uppercase text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-400 drop-shadow-2xl">
        Split Search
      </h1>
      <form @submit.prevent="executeSearch" class="w-full max-w-2xl relative">
        <input
          v-model="query"
          type="text"
          class="w-full bg-white text-black text-lg md:text-xl px-6 py-4 rounded-full shadow-2xl border-4 border-transparent focus:outline-none focus:border-zinc-500 transition-all placeholder-gray-400 font-bold"
          placeholder="Type to search..."
          required
        />
        <button type="submit" class="absolute right-2 top-2 bottom-2 px-8 bg-black text-white font-black rounded-full hover:bg-zinc-800 transition-colors uppercase tracking-widest text-sm border border-zinc-700 shadow-lg">
          Search
        </button>
      </form>
    </div>

    <div v-else class="min-h-screen flex flex-col">

      <header class="p-4 md:p-6 bg-black/80 backdrop-blur-md border-b border-zinc-800 sticky top-0 z-10 flex flex-col md:flex-row items-center gap-4 md:gap-8 shadow-xl">
        <h1 class="text-2xl md:text-3xl font-black tracking-tighter uppercase cursor-pointer hover:text-gray-300 transition-colors" @click="resetSearch">
          Split Search
        </h1>
        <form @submit.prevent="executeSearch" class="flex-1 w-full max-w-3xl relative">
          <input
            v-model="query"
            type="text"
            class="w-full bg-white text-black px-6 py-3 rounded-full shadow-inner focus:outline-none focus:ring-4 focus:ring-zinc-600 font-bold"
            required
          />
          <button type="submit" class="absolute right-1.5 top-1.5 bottom-1.5 px-6 bg-black text-white font-bold rounded-full hover:bg-zinc-800 transition-colors text-xs uppercase tracking-wider">
            Search
          </button>
        </form>
      </header>

      <div class="flex-1 grid grid-cols-1 md:grid-cols-2 gap-8 p-6 lg:p-10">

        <div class="flex flex-col gap-5">
          <div class="flex justify-between items-end mb-2 border-b-2 border-zinc-800/50 pb-3">
            <h2 class="text-xl md:text-2xl font-black uppercase tracking-widest text-white drop-shadow-md">Elasticsearch <span class="text-zinc-300">+ PR</span></h2>
            <div class="text-sm font-mono text-zinc-200 text-right bg-black/30 px-3 py-1 rounded-md">
              <p v-if="esLoading" class="animate-pulse">Loading...</p>
              <p v-else>Hits: {{ esTotal }} | Time: {{ esTime }}s</p>
            </div>
          </div>

          <div v-if="!esLoading" class="flex flex-col gap-5">
            <div v-for="(item, index) in esResults" :key="index" class="bg-white text-black p-5 rounded-none shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 hover:translate-x-1 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all border-2 border-black group">
              <a :href="item.url" target="_blank" class="text-blue-700 text-lg md:text-xl font-black group-hover:underline line-clamp-1 decoration-4 underline-offset-4">{{ item.title }}</a>
              <p class="text-emerald-700 font-mono text-xs md:text-sm mt-1 mb-3 break-all font-bold">{{ item.url }}</p>
              <p class="text-zinc-700 text-sm md:text-base line-clamp-2 leading-relaxed font-medium">{{ item.snippet }}</p>
              <div class="mt-4 pt-3 border-t-2 border-zinc-200 flex justify-between items-center">
                <span class="text-xs font-black text-white bg-black px-3 py-1 uppercase tracking-widest shadow-sm">Rank #{{ index + 1 }}</span>
                <span class="text-xs font-bold text-zinc-500">Score: {{ parseFloat(item.score).toFixed(4) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="flex flex-col gap-5">
          <div class="flex justify-between items-end mb-2 border-b-2 border-zinc-800/50 pb-3">
            <h2 class="text-xl md:text-2xl font-black uppercase tracking-widest text-white drop-shadow-md">Manual TF-IDF <span class="text-zinc-300">+ PR</span></h2>
            <div class="text-sm font-mono text-zinc-200 text-right bg-black/30 px-3 py-1 rounded-md">
              <p v-if="manualLoading" class="animate-pulse">Loading...</p>
              <p v-else>Hits: {{ manualTotal }} | Time: {{ manualTime }}s</p>
            </div>
          </div>

          <div v-if="!manualLoading" class="flex flex-col gap-5">
            <div v-for="(item, index) in manualResults" :key="index" class="bg-white text-black p-5 rounded-none shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:-translate-y-1 hover:translate-x-1 hover:shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] transition-all border-2 border-black group">
              <a :href="item.url" target="_blank" class="text-blue-700 text-lg md:text-xl font-black group-hover:underline line-clamp-1 decoration-4 underline-offset-4">{{ item.title }}</a>
              <p class="text-emerald-700 font-mono text-xs md:text-sm mt-1 mb-3 break-all font-bold">{{ item.url }}</p>
              <p class="text-zinc-700 text-sm md:text-base line-clamp-2 leading-relaxed font-medium">{{ item.snippet }}</p>
              <div class="mt-4 pt-3 border-t-2 border-zinc-200 flex justify-between items-center">
                <span class="text-xs font-black text-white bg-black px-3 py-1 uppercase tracking-widest shadow-sm">Rank #{{ index + 1 }}</span>
                <span class="text-xs font-bold text-zinc-500">Score: {{ parseFloat(item.score).toFixed(4) }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const query = ref('')
const hasSearched = ref(false)

const esResults = ref([])
const esTotal = ref(0)
const esTime = ref(0)
const esLoading = ref(false)

const manualResults = ref([])
const manualTotal = ref(0)
const manualTime = ref(0)
const manualLoading = ref(false)

const executeSearch = async () => {
  if (!query.value.trim()) return
  hasSearched.value = true

  esLoading.value = true
  manualLoading.value = true

  try {
    const resES = await fetch(`http://127.0.0.1:5000/api/search_es?q=${encodeURIComponent(query.value)}`)
    const dataES = await resES.json()
    esResults.value = dataES.results || []
    esTotal.value = dataES.total_results || 0
    esTime.value = dataES.execution_time || 0
  } catch (err) {
    console.error('ES Search Error:', err)
  } finally {
    esLoading.value = false
  }

  try {
    const resManual = await fetch(`http://127.0.0.1:5000/api/search_manual?q=${encodeURIComponent(query.value)}`)
    const dataManual = await resManual.json()
    manualResults.value = dataManual.results || []
    manualTotal.value = dataManual.total_results || 0
    manualTime.value = dataManual.execution_time || 0
  } catch (err) {
    console.error('Manual Search Error:', err)
  } finally {
    manualLoading.value = false
  }
}

const resetSearch = () => {
  hasSearched.value = false
  query.value = ''
  esResults.value = []
  manualResults.value = []
}
</script>