<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Generador de Hipervectores ADN</h1>
    <input
      v-model="sequence"
      type="text"
      class="border border-gray-300 rounded p-2 mb-4 w-full"
      placeholder="Ingrese secuencia de ADN (G, T, K, A)"
    />
    <button
      @click="generateHV"
      class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
    >
      Generar Hipervector
    </button>
    <div v-if="error" class="text-red-500 mt-4">{{ error }}</div>
    <div v-if="hypervector" class="mt-4">
      <h2 class="text-xl font-semibold">Hipervector generado:</h2>
      <pre class="bg-gray-100 p-2 rounded">{{ hypervector }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const sequence = ref("");
const hypervector = ref(null);
const error = ref(null);

const generateHV = async () => {
  hypervector.value = null;
  error.value = null;

  try {
    console.log(sequence.value);
    const post = { sequence: sequence.value };
    console.log(post);

    const response = await axios.post(
      "http://127.0.0.1:8000/generate-hv",
      post
    );

    console.log(response.data);

    if (response.data.error) {
      error.value = response.data.error;
    } else {
      hypervector.value = response.data.hypervector;
    }
  } catch {
    error.value = "Error al comunicarse con el servidor.";
  }
};
</script>

<style>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
