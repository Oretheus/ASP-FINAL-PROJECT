<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center q-px-md q-py-lg">
        <div class="flex justify-end">
          <q-toggle
            v-model="collectionStore.darkMode"
            color="blue"
            label="Mode"
            left-label
          />
        </div>
        <q-card
          class="q-pa-lg shadow-2"
          :style="{
            width: '400px',
            maxWidth: '90%',
            height: '600px',
            borderRadius: '10px',
            background: collectionStore.darkMode
              ? 'linear-gradient(135deg, #333, #555)'
              : 'linear-gradient(135deg, #286ea6, #1a4d80)',
          }"
        >
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
              If you already have an account, login below
            </div>
          </div>

          <!-- Form -->
          <q-card
            style="
              border-radius: 10px;
              margin-top: 50px;
              padding: 20px;
              box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            "
          >
            <q-form @submit="onSubmit">
              <q-input
                dense
                outlined
                v-model="email"
                type="email"
                label="Email *"
                style="border-radius: 5px; margin-bottom: 10px; color: black"
                hint="Enter your email"
                :rules="[isValidEmail, 'Enter a valid email address.']"
              />
              <q-input
                dense
                outlined
                v-model="password"
                :type="passwordVisible ? 'text' : 'password'"
                label="Password *"
                :rules="[(val) => !!val || 'Password is required.']"
                style="border-radius: 5px; margin-bottom: 10px; color: black"
              >
                <template v-slot:append>
                  <q-icon
                    :name="passwordVisible ? 'visibility_off' : 'visibility'"
                    @click="togglePasswordVisibility"
                    class="cursor-pointer"
                    color="black"
                  />
                </template>
              </q-input>

              <q-btn
                type="submit"
                label="Login"
                :loading="loading"
                style="
                  color: white;
                  width: 100%;
                  margin-bottom: 10px;
                  background-color: #4b88c4;
                  border-radius: 5px;
                  padding: 10px 20px;
                "
              />
              <div class="text-right">
                <q-btn
                  flat
                  color="red"
                  label="Forgot Password?"
                  @click="handleRegister"
                  style="color: white; font-size: 10px"
                />
              </div>
              <q-banner
                v-if="errorMessage"
                dense
                color="negative"
                style="margin-top: 10px"
              >
                {{ errorMessage }}
              </q-banner>
            </q-form>
            <div class="text-center" style="color: #1976d2; font-size: 13px">
              <p>If you do not have an account, please register.</p>
              <q-btn
                flat
                label="Register"
                @click="handleRegister"
                style="color: #1976d2; font-size: 12px"
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
import { useRouter } from "vue-router";
import axios from "axios";

const email = ref("demo123@email.com");
const password = ref("Password123");
const passwordVisible = ref(false);
const errorMessage = ref("");
const loading = ref(false);
const router = useRouter();
import { useCollectionStore } from "@/stores/mycore";
const collectionStore = useCollectionStore();

const handleRegister = () => {
  router.push("/");
};

function onSubmit() {
  console.log("Email:", email.value);
  console.log("Password:", password.value);

  if (!isValidEmail(email.value) || !password.value) {
    errorMessage.value =
      "Please fill in all required fields with valid values.";
    return;
  }

  const dataObj = new URLSearchParams();
  dataObj.append("username", email.value);
  dataObj.append("password", password.value);

  axios
    .post("https://asp-final-project.onrender.com/v1/user/login", dataObj, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    })
    .then((response) => {
      if (response.data && response.data.access_token) {
        localStorage.setItem("authToken", response.data.access_token);
        router.push("/candidate1");
      } else {
        errorMessage.value = "Unexpected response format.";
      }
    })
    .catch((error) => {
      errorMessage.value =
        error.response?.data?.message || "Login failed. Please try again.";
    });
}

function togglePasswordVisibility() {
  passwordVisible.value = !passwordVisible.value;
}

const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
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
