<template>
  <div>
    <canvas id="myChart"></canvas>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

export default {
  props: {
    hypervector: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const chartRef = ref(null);

    onMounted(() => {
      const ctx = chartRef.value.getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: props.hypervector.map((_, i) => i),
          datasets: [
            {
              label: "Hipervector",
              data: props.hypervector,
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: "Índice",
              },
            },
            y: {
              title: {
                display: true,
                text: "Valor",
              },
            },
          },
        },
      });
    });

    return {
      chartRef,
    };
  },
};
</script>
