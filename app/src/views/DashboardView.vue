<template>
    <div class="grid grid-cols-10">
  
      <!--Heatmap-->
      <div ref="heatmapContainer" class="heatmap col-span-8 h-screen bg-zinc-800 justify-items-center">
        <heatmap />
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
              <div><h1 class="text-7xl text-white mt-3"><span v-text="distanciaJogador"></span></h1></div>
              <h1 class="mt-2 text-3xl text-zinc-600">m</h1>
            </div>
          </div>
  
          <div class="grid grid-flow-row pt-5 p-4  border-t border-zinc-800 justify-items-start">
            <div class="text-zinc-500">
              <h1>Velocidade do atleta</h1>
            </div>
            <div class="grid grid-cols-2 gap-2 justify-items-start">
              <div><h1 class="text-7xl text-white mt-3"><span v-text="speedJogador"></span></h1></div>
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
  import axios from 'axios';
  import heatmap from 'heatmap.js'

  export default {
    name: 'DashboardView',
    components: {
      heatmap
    },
    props: {},
    
    data() {
      return {
        distanciaJogador: 0,
        speedJogador: 0,
        heatmapValues: [],
        heatmapInstance: null
      };
    },
    mounted() {
      this.heatmapInstance = heatmap.create({
        container: this.$refs.heatmapContainer,
        radius: 80,
        blur: 0.95,
        width: 1600,
        height: 1000,
        minOpacity: 0,
        maxOpacity: 0.5,
        gradient: {
          '.3': 'blue',
          '.5': 'green',
          '.8': 'yellow',
          '1': 'red'
        }
      });

      this.heatmapInstance.setData({
        data: [
          {x: 100, y: 80, value: 200},
          // adicione mais dados aqui...
        ]
      });

      setInterval(this.requisicaoDistancia, 1500);
      setInterval(this.requisicaoSpeed, 1500);
      setInterval(this.requisicaoHeatmap, 3000);
    },
    methods: {
      async requisicaoDistancia() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/distance');
          const payload = response.data;
          this.distanciaJogador = payload.d_player.toFixed(2);
        } catch (error) {
          console.error(error);
        }
      },
      async requisicaoSpeed() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/speed');
          const payload = response.data;
          console.log(payload);
        } catch (error) {
          console.error(error);
        }
      },

      async requisicaoHeatmap() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/heatmap');
          const payload = response.data;
          console.log('heatmap ',payload.d_player);
          this.heatmapInstance.setData({
            data: payload.d_player
          });
        } catch (error) {
          console.error(error);
        }
      },

    }
  }
</script>



  
  