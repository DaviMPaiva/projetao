<template>
    <div class="grid grid-cols-10">
  
      <!--Heatmap-->
      <div ref="heatmapContainer" class="heatmap col-span-8 h-screen bg-zinc-800 justify-items-center">
        <div ref="heatmapContainer"></div>
      </div>
  
      <!--Painel de controle-->
      <div class="col-span-2 px-10 h-screen bg-zinc-900 pt-10">
  
        <div class="grid grid-rows gap-4">
          <div class="grid grid-flow-row justify-items-end">
            <div class="text-zinc-600 hover:text-lime-400 font-bold">
              <button>
                
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
                </svg>
              </button>
            </div>
          </div>
  
          <div class="grid grid-flow-row gap-4 justify-items-start">
            <div class="text-zinc-500">
              <h1>Selecione o atleta</h1>
            </div>
            <div class="grid grid-cols-2 gap-2 justify-items-start">
              <button class="font-bold text-zinc-900 bg-lime-400 h-10 w-full px-10 rounded-full">Jogador</button>
              <button class="font-bold text-zinc-900 bg-lime-400 h-10 w-full px-10 rounded-full">Adversário</button>
            </div>
          </div>
  
          <div class="grid grid-flow-row pt-5 p-4 border-t border-zinc-800 justify-items-start">
            <div class="text-zinc-500">
              <h1>Aceleração média do atleta</h1>
            </div>
            <div class="grid grid-cols-2 gap-2 justify-items-start">
              <div><h1 class="text-7xl text-white mt-3">X</h1></div>
              <h1 class="mt-2 text-3xl text-zinc-600">m/s</h1>
            </div>
          </div>
  
          <div class="grid grid-flow-row pt-5 p-4  border-t border-zinc-800 justify-items-start">
            <div class="text-zinc-500">
              <h1>Distância percorrida</h1>
            </div>
            <div class="grid grid-cols-2 gap-2 justify-items-start">
              <div><h1 class="text-7xl text-white mt-3">X</h1></div>
              <h1 class="mt-2 text-3xl text-zinc-600">m</h1>
            </div>
          </div>
  
          <div class="grid grid-flow-row pt-5 p-4  border-t border-zinc-800 justify-items-start">
            <div class="text-zinc-500">
              <h1>Velocidade do atleta</h1>
            </div>
            <div class="grid grid-cols-2 gap-2 justify-items-start">
              <div><h1 class="text-7xl text-white mt-3">X</h1></div>
              <h1 class="mt-2 text-3xl text-zinc-600">m/s</h1>
            </div>
          </div>
  
          <div class="grid grid-flow-row pt-5 p-4 gap-5  border-t border-zinc-800 justify-items-start">
            <div class="text-zinc-500">
              <h1>Tempo de jogo</h1>
            </div>
            <div class="grid grid-cols-2 justify-items-start">
              <div><h1 class="text-1xl text-white"><strong>25</strong> <span class="text-zinc-500">minutos</span></h1></div>
              <div><h1 class="text-1xl text-white"><strong>13</strong> <span class="text-zinc-500">segundos</span></h1></div>
            </div>
          </div>
  
          <div class="grid grid-flow-row p-4  pt-20 justify-items-center">
            <div>
              <img src="../assets/logotipoSvg.svg" class="" alt="Minha imagem">
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
  
<style>
  
  .heatmap {
    background-image: url('../assets/Group-3.svg');
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center top;
   
  }
  
</style>
  
<script>
  import heatmap from 'heatmap.js'
  
  
  export default {
    name: 'DashboardView',
    props: {
  
    },
    mounted() {
      const heatmapInstance = heatmap.create({
        
        container: this.$refs.heatmapContainer,
        radius: 250,
        maxOpacity: 0.7,
        blur: 0.80,
        gradient: {
          '.3': 'blue',
          '.5': 'green',
          '.8': 'yellow',
          '1': 'red'
        }
      })
  
      heatmapInstance.setData({
        data: [
          {x: 100, y: 80, value: 200},
          {x: 500, y: 800, value: 200},
          {x: 900, y: 500, value: 90},
          {x: 1000, y: 300, value: 110},
          {x: 400, y: 500, value: 120},
          {x: 100, y: 500, value: 60},
          {x: 800, y: 700, value: 40},
          {x: 200, y: 800, value: 90},
          {x: 500, y: 100, value: 100},
          {x: 1000, y: 600, value: 110},
          {x: 100, y: 200, value: 110},
          {x: 700, y: 800, value: 120},
          {x: 900, y: 300, value: 100},
          {x: 500, y: 600, value: 80},
          {x: 200, y: 100, value: 70}
  
          // adicione mais dados aqui...
        ]
      })
    }
  }
</script>
  
  
  