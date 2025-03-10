import { ref, computed, watch } from "vue";
import axios from "axios";
import _ from "lodash";
import { onMounted } from 'vue';
import { defineStore } from "pinia";
import { Dark } from "quasar";

export const useCollectionStore = defineStore('mycore', () => {
  const darkMode = ref(Dark.isActive); // Initialize with the current dark mode state

  watch(darkMode, (newVal) => {
    Dark.set(newVal); // Update the dark mode state
  });

  return {
    darkMode,
  };
});
