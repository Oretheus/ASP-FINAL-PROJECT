<template>
    <router-view></router-view>
    <!-- <CandidatePage></CandidatePage> -->
   
</template>

<script setup>
import { ref } from "vue";
import Login from "@/components/Login.vue";
import CandidatePage1 from "@/components/CandidatePage1.vue";
import CandidatePage2 from "@/components/CandidatePage2.vue";
// import { useCollectionStore } from "@/stores/mycore";
// const collectionStore = useCollectionStore();
// collectionStore.mainActiveComponentName = "MainRegistration";

</script>

<style scoped></style>