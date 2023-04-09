<template>
    <div class="bg-zinc-900 flex justify-center items-center h-screen">
        
        <div class="w-1/4">
            <h1 class="text-1xl mb-5 text-zinc-500">Insira o IPV4 das câmeras</h1>
            <input type="text" v-model="camera1" class="mb-6 bg-zinc-800 border border-zinc-700 text-zinc-400 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="IPV4 da câmera 1"> 
            <input type="text" v-model="camera2" class="bg-zinc-800 border border-zinc-700 text-zinc-400 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5" placeholder="IPV4 da câmera 2" >
            <button @click="enviarPedidoPost" class="bg-lime-400 px-10 mt-4 py-2 rounded-full text-zinc-800 font-bold">Confirmar</button>
        </div>

    </div>
</template>

<style>
  
</style>
  
<script>
import axios from 'axios';

export default {
  data() {
    return {
      camera1: '',
      camera2: ''
    };
  },
  methods: {
    enviarPedidoPost() {
      const data = {
        camera1: this.camera1,
        camera2: this.camera2
      };
      axios.post('http://127.0.0.1:5000/cam-ip', data)
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>
  
  
  