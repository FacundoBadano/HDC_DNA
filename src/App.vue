<template>
  <div
    class="flex flex-col justify-center items-center min-h-screen bg-gray-100"
  >
    <div class="w-3/5 bg-white p-8 shadow-lg rounded-lg space-y-6">
      <h1 class="text-3xl font-bold text-center">
        Calculadora de Distancia entre Secuencias ADN
      </h1>

      <div class="bg-blue-500 text-white p-4 rounded text-center">
        Indicar ambas secuencias para calcular su distancia.
      </div>

      <!-- Input de la secuencia original -->
      <input
        v-model="sequence1"
        type="text"
        class="border border-gray-300 rounded p-3 w-full"
        placeholder="Ingrese la secuencia original de ADN (G, T, C, A)"
      />

      <!-- Opción para perturbar la secuencia -->
      <div class="flex items-center space-x-3">
        <input
          type="checkbox"
          v-model="perturbate"
          class="w-5 h-5"
          @change="handlePerturbationChange"
        />
        <label class="text-lg">Perturbar la secuencia original</label>
      </div>

      <!-- Input de porcentaje de perturbación (solo visible si perturbate es true) -->
      <div v-if="perturbate" class="flex items-center space-x-3">
        <label class="text-lg">Porcentaje de perturbación:</label>
        <input
          v-model="perturbationPercentage"
          type="number"
          min="1"
          max="100"
          class="border border-gray-300 rounded p-2 w-20"
          @input="generatePerturbedSequence"
        />
      </div>

      <!-- Input de la segunda secuencia (rellenado automáticamente si perturbate es true) -->
      <input
        v-model="sequence2"
        type="text"
        class="border border-gray-300 rounded p-3 w-full"
        placeholder="Ingrese la segunda secuencia de ADN (G, T, C, A)"
        :readonly="perturbate"
      />

      <!-- Botón para calcular distancia -->
      <button
        @click="calculateDistance"
        class="bg-blue-500 text-white px-6 py-3 rounded hover:bg-blue-600 w-full"
      >
        Calcular Distancia
      </button>

      <!-- Mostrar error si hay -->
      <div v-if="error" class="text-red-500 text-center">{{ error }}</div>

      <!-- Mostrar distancia calculada -->
      <div v-if="distance !== null" class="mt-4">
        <h2 class="text-xl font-semibold text-center">Distancia Calculada:</h2>
        <p class="bg-gray-100 p-3 rounded text-center">{{ distance }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// Variables reactivas
const sequence1 = ref("");
const sequence2 = ref("");
const perturbate = ref(false);
const perturbationPercentage = ref(5);
const distance = ref(null);
const error = ref(null);

// Función para perturbar la cadena original
const perturbSequence = (sequence, percentage) => {
  let seqArray = sequence.split("");
  let numChanges = Math.ceil(seqArray.length * (percentage / 100));
  const validChars = ["G", "T", "C", "A"];

  for (let i = 0; i < numChanges; i++) {
    let index = Math.floor(Math.random() * seqArray.length);
    let newChar;
    do {
      newChar = validChars[Math.floor(Math.random() * validChars.length)];
    } while (newChar === seqArray[index]); // Asegurar que el carácter cambie
    seqArray[index] = newChar;
  }

  return seqArray.join("");
};

// Función para generar y mostrar la cadena perturbada
const generatePerturbedSequence = () => {
  if (perturbate.value && sequence1.value) {
    sequence2.value = perturbSequence(
      sequence1.value,
      perturbationPercentage.value
    );
  }
};

// Función que se ejecuta al cambiar el checkbox de perturbación
const handlePerturbationChange = () => {
  if (perturbate.value) {
    generatePerturbedSequence();
  } else {
    sequence2.value = ""; // Limpiar el segundo input si se desactiva la perturbación
  }
};

// Función para calcular la distancia
const calculateDistance = async () => {
  distance.value = null;
  error.value = null;

  if (!sequence1.value) {
    error.value = "Por favor, ingrese la secuencia original.";
    return;
  }

  let seq2ToSend = sequence2.value;

  if (perturbate.value) {
    if (
      perturbationPercentage.value < 1 ||
      perturbationPercentage.value > 100
    ) {
      error.value = "El porcentaje de perturbación debe estar entre 1 y 100.";
      return;
    }
    // La cadena perturbada ya fue generada y mostrada en sequence2
    seq2ToSend = sequence2.value;
  } else if (!sequence2.value) {
    error.value = "Por favor, ingrese la segunda secuencia.";
    return;
  }

  try {
    const response = await axios.post("http://127.0.0.1:8000/generate-hv", {
      sequence1: sequence1.value,
      sequence2: seq2ToSend,
    });

    distance.value = response.data.distance.toFixed(4);
  } catch (err) {
    error.value =
      err.response?.data?.detail || "Error al comunicarse con el servidor.";
  }
};
</script>
