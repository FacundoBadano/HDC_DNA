<template>
  <div id="app">
    <InputSequence @submit="generateHypervector" />
    <HypervectorDisplay :hypervector="hypervector" />
  </div>
</template>

<script>
import InputSequence from "./components/InputSequence.vue";
import HypervectorDisplay from "./components/HypervectorDisplay.vue";

export default {
  name: "App",
  components: {
    InputSequence,
    HypervectorDisplay,
  },
  data() {
    return {
      hypervector: null,
    };
  },
  methods: {
    generateHypervector(sequence) {
      fetch("/generate_hdc", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sequence }),
      })
        .then((response) => response.json())
        .then((data) => {
          this.hypervector = data.hypervector;
        });
    },
  },
};
</script>
