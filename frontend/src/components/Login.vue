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
              : 'linear-gradient(135deg, #286ea6, #1a4d80)',
          }"
        >
          <!-- linear-gradient(135deg, #4e54c8, #8f94fb) -->
          <!-- Header -->
          <div class="text-center q-mb-md">
            <q-avatar size="80px">
              <img
                src="@/assets/earth.png"
                alt="Earth Icon"
                class="earth-icon"
              />
            </q-avatar>
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
                    :color="passwordVisible ? 'red' : '#fff'"
                  />
                </template>
              </q-input>

              <q-btn
                type="submit"
                label="Login"
                :loading="loading"
                :style="{
                  color: 'white',
                  width: '100%',
                  marginBottom: '10px',
                  backgroundColor: '#4b88c4',
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
import Register from "@/components/Register.vue";
import { useRouter } from "vue-router";
import axios from "axios";
// import { useQuasar } from "quasar";
const email = ref("asd@gmail.com");
const password = ref("Password123");
const passwordVisible = ref(false);
const darkMode = ref(false);
const errorMessage = ref("");
const loading = ref(false);
const router = useRouter();

const handleRegister = () => {
  router.push("/");
};

function onSubmit() {
  console.log("Email:", email.value);
  console.log("Password:", password.value);

  // Validate inputs
  if (!isValidEmail(email.value) || !password.value) {
    errorMessage.value =
      "Please fill in all required fields with valid values.";
    console.error("Validation Error:", errorMessage.value);
    return;
  }

  // Request payload (using URLSearchParams to encode the data for x-www-form-urlencoded)
  const dataObj = new URLSearchParams();
  dataObj.append("username", email.value); 
  dataObj.append("password", password.value); 

  axios
    .post("https://asp-final-project.onrender.com/v1/user/login", dataObj, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    })
    .then(function (response) {
      console.log("Login Response:", response.data);

      // Handle success
      if (response.data && response.data.access_token) {
        console.log(response.data.message);
        localStorage.setItem("authToken", response.data.access_token);

        const storedToken = localStorage.getItem("authToken");
        console.log("Stored Token:", storedToken);

        // Redirect user
        router.push("/candidate1");
      } else {
        errorMessage.value = "Unexpected response format.";
        console.warn("Unexpected Response Format:", response.data);
      }
    })
    .catch(function (error) {
      // Handle error
      console.error("Login Failed:", error.response?.data || error.message);
      errorMessage.value =
        error.response?.data?.message || "Login failed. Please try again.";
    });
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
/* .q-input {
  border-radius: 130px;
  background-color: rgba(255, 255, 255, 0.1);
} */
</style>
