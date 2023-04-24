<template>
    <div class="flex flex-column">
  
      <!--Heatmap-->
      <div  class="h-screen bg-zinc-800 flex items-center">
        <div ref="heatmapContainer1" v-show="exibirPlayerUm" class="heatmap w-[1600px] h-[1000px] border-2 border-green-500">teste1<heatmap/></div>
        <div ref="heatmapContainer2" v-show="exibirPlayerDois" class="heatmap w-[1600px] h-[1000px] border-2 border-pink-500">teste2<heatmap/></div>
      </div>

        
      <!--Painel de controle-->
      <div class="bg-zinc-900 w-[20vw] px-10 py-10">
  
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
            <div class="grid grid-cols-2 gap-2">
              <button @click="exibirPlayer1" class="font-bold border border-lime-400 text-white h-10 w-full px-10 rounded-full focus:bg-lime-400 focus:text-zinc-900">Jogador</button>
              <button @click="exibirPlayer2" class="font-bold border border-lime-400 text-white h-10 w-full px-10 rounded-full focus:bg-lime-400 focus:text-zinc-900">Adversário</button>
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
        distanciaJogador1: 0,
        speedJogador1: 0,
        heatmapValues1: [],
        heatmapInstance1: null,
        distanciaJogador2: 0,
        speedJogador2: 0,
        heatmapValues2: [],
        heatmapInstance2: null,
        exibirPlayerUm: true,
        exibirPlayerDois: false,
      };
    },
    mounted() {
      this.heatmapInstance1 = heatmap.create({
        container: this.$refs.heatmapContainer1,
        radius: 80,
        blur: 0.95,
        minOpacity: 0,
        maxOpacity: 0.5,
        gradient: {
          '.3': 'blue',
          '.5': 'green',
          '.8': 'yellow',
          '1': 'red'
        }
      });

      this.heatmapInstance2 = heatmap.create({
        container: this.$refs.heatmapContainer2,
        radius: 80,
        blur: 0.95,
        minOpacity: 0,
        maxOpacity: 0.5,
        gradient: {
          '.3': 'blue',
          '.5': 'green',
          '.8': 'yellow',
          '1': 'red'
        }
      });

      this.heatmapInstance1.setData({
        data: [
          {x: 100, y: 80, value: 200},
          // adicione mais dados aqui...
        ]
      });
      
      this.heatmapInstance2.setData({
        data: [
          {x: 200, y: 200, value: 200},
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
          this.distanciaJogador1 = payload.d_player.toFixed(2);
          this.distanciaJogador2 = payload.d_opponent.toFixed(2);
        } catch (error) {
          console.error(error);
        }
      },
      async requisicaoSpeed() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/speed');
          const payload = response.data;
          this.speedJogador1 = payload.d_player.toFixed(0);
          this.speedJogador2 = payload.d_opponent.toFixed(0);
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
          this.heatmapInstance1.setData({
            data: payload.d_player
          });
           this.heatmapInstance2.setData({
            data: payload.d_opponent
          });
        } catch (error) {
          console.error(error);
        }
      },

      exibirPlayer1() {
        this.exibirPlayerUm = true;
        this.exibirPlayerDois = false;
        console.log('player1 ativo')
      },
      exibirPlayer2() {
        this.exibirPlayerUm = false;
        this.exibirPlayerDois = true;
        console.log('player2 ativo')
      },

    }
  }
</script>



  
  