<template>
  <div class="p-24">
    <h1 class="text-2xl font-bold mb-4 text-center">
      Calculadora de Distancia entre Secuencias ADN
    </h1>

    <div class="bg-blue-500 text-white p-4 rounded">
      Indicar ambas secuencias para calcular su distancia.
    </div>

    <input
      v-model="sequence1"
      type="text"
      class="border border-gray-300 rounded p-2 mb-4 w-full"
      placeholder="Ingrese la primera secuencia de ADN (G, T, C, A)"
    />

    <input
      v-model="sequence2"
      type="text"
      class="border border-gray-300 rounded p-2 mb-4 w-full"
      placeholder="Ingrese la segunda secuencia de ADN (G, T, C, A)"
    />

    <button
      @click="calculateDistance"
      class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
    >
      Calcular Distancia
    </button>

    <div v-if="error" class="text-red-500 mt-4">{{ error }}</div>
    <div v-if="distance !== null" class="mt-4">
      <h2 class="text-xl font-semibold">Distancia Calculada:</h2>
      <p class="bg-gray-100 p-2 rounded">{{ distance }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const sequence1 = ref("");
const sequence2 = ref("");
const distance = ref(null);
const error = ref(null);

const calculateDistance = async () => {
  distance.value = null;
  error.value = null;

  if (!sequence1.value || !sequence2.value) {
    error.value = "Por favor, ingrese ambas secuencias.";
    return;
  }

  try {
    const response = await axios.post("http://127.0.0.1:8000/generate-hv", {
      sequence1: sequence1.value,
      sequence2: sequence2.value,
    });

    distance.value = response.data.distance.toFixed(4);
  } catch (err) {
    error.value =
      err.response?.data?.detail || "Error al comunicarse con el servidor.";
  }
};
</script>

<style>
pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
