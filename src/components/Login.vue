<template>
  <div class="absolute top-0 left-0 q-mt-md q-ml-md" style="z-index: 1">
    <q-toggle
      dense
      v-model="darkMode"
      label="Dark Mode"
      color="white"
      @change="toggleDarkMode"
      :style="{ width: 'auto' }"
    />
  </div>

  <q-layout :class="{ 'bg-dark': darkMode, 'bg-light': !darkMode }">
    <q-page-container>
      <q-page
        class="flex flex-center q-px-md q-py-lg"
        :style="{
          background: darkMode ? '#333' : '#fff',
          color: darkMode ? '#fff' : '#000',
        }"
      >
        <q-card
          class="q-pa-lg shadow-2"
          :style="{
            width: '400px',
            maxWidth: '90%',
            height: '600px',
            borderRadius: '10px',
            background: darkMode
              ? 'linear-gradient(to right, #333, #444)'
              : 'linear-gradient(to right, #6a11cb, #2575fc)',
          }"
        >
          <!-- Header -->
          <div class="text-center q-mb-md">
            <q-icon name="public" size="80px" color="white" />
            <div class="text-h6 text-white">Welcome</div>
            <div class="text-body2 text-white">
              If you already have an account login
            </div>
          </div>

          <!-- Form -->
          <q-card
            :style="{
              backgroundColor: darkMode ? '#333' : '#fff',
              borderRadius: '10px',
              marginTop: '50px',
              padding: '20px',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
            }"
          >
            <q-form @submit="onSubmit">
              <q-input
                dense
                outlined
                v-model="email"
                type="email"
                label="Email *"
                :style="{
                  background: darkMode ? 'grey' : 'white',
                  borderRadius: '5px',
                  marginBottom: '10px',
                  color: darkMode ? '#fff' : '#000',
                }"
                hint="Enter your username"
                :rules="[
                  (val) => !!val || 'Email is required.',
                  (val) => isValidEmail(val) || 'Enter a valid email address.',
                ]"
              />
              <q-input
                dense
                outlined
                v-model="password"
                :type="passwordVisible ? 'text' : 'password'"
                label="Password *"
                :rules="[(val) => !!val || 'Password is required.']"
                :style="{
                  background: darkMode ? 'grey' : 'white',
                  borderRadius: '5px',
                  marginBottom: '10px',
                  color: darkMode ? '#fff' : '#000',
                }"
              >
                <template v-slot:append>
                  <q-icon
                    :name="passwordVisible ? 'visibility_off' : 'visibility'"
                    @click="togglePasswordVisibility"
                    class="cursor-pointer"
                  />
                </template>
              </q-input>

              <q-btn
                type="submit"
                label="Login"
                :loading="loading"
                :style="{
                  color: 'black',
                  width: '100%',
                  marginBottom: '10px',
                  backgroundColor: '#1976d2',
                  borderRadius: '5px',
                  padding: '10px 20px',
                }"
              />
              <div class="text-right">
                <q-btn
                  flat
                  color="red"
                  label="Forgot Password?"
                  @click="handleRegister"
                  :style="{ color: 'white', fontSize: '10px' }"
                />
              </div>
              <q-banner
                v-if="errorMessage"
                dense
                color="negative"
                :style="{ marginTop: '10px' }"
              >
                {{ errorMessage }}
              </q-banner>
            </q-form>
            <div
              :style="{
                color: darkMode ? 'white' : '#1976d2',
                fontSize: '13px',
              }"
              class="text-center"
            >
              <p>
                If you do not have an account, please register to create one.
              </p>

              <q-btn
                flat
                label="Register"
                @click="handleRegister"
                :style="{
                  color: darkMode ? 'white' : '#1976d2',
                  fontSize: '12px',
                }"
              />
            </div>
          </q-card>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import RegisterPage from "@/components/RegisterPage.vue"; //changed path 23/01
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const passwordVisible = ref(false);
const darkMode = ref(false);
const errorMessage = ref("");
const loading = ref(false);
const router = useRouter();

const navigateToLogin = () => {
  router.push("/Login");
};

const handleRegister = () => {
  router.push("/RegisterPage"); //changed path 23/01
};

function onSubmit() {
  const url = "";
  const dataObj = {
    username: email.value,
    password: password.value,
  };
}

function togglePasswordVisibility() {
  passwordVisible.value = !passwordVisible.value;
}

function toggleDarkMode() {
  darkMode.value = !darkMode.value;
}
const isValidEmail = (value) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(value);
};
</script>

<style scoped>
.q-page {
  position: relative;
  overflow: hidden;
}
.q-card {
  backdrop-filter: blur(5px);
  box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.2);
}
</style>
