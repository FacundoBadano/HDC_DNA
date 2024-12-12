<template>
  <form @submit.prevent="handleSubmit">
    <input
      type="text"
      v-model="sequence"
      placeholder="Ingrese la secuencia de ADN"
    />
    <button type="submit">Generar Hipervector</button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      sequence: "",
    };
  },
  methods: {
    handleSubmit() {
      this.$emit("submit", this.sequence);
    },
  },
};
</script>
