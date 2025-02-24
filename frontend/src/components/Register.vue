<template>
  <div class="registration-container">
    <!-- Login Redirect Button -->
    <button class="login-btn" @click="redirectToLogin">Login</button>

    <!-- Form Layout -->
    <div class="form-layout">
      <!-- Left Section with Image and Text -->
      <div class="left-section">
        <div class="symbol-container">
          <img src="@/assets/earth.png" alt="Earth Icon" class="earth-icon" />
          <p>
            The only place to make applying for internships, fun and rewarding
          </p>
          <p>Register here to make the world your oyster!</p>
        </div>
      </div>

      <!-- Right Section with Registration Form -->
      <div class="form-section">
        <h2>Register</h2>
        <q-form @submit.prevent="handleRegister">
          <q-input
            v-model="name"
            label="First Name *"
            dense
            outlined
            :rules="[(val) => !!val || 'Name is required.']"
          />
          <q-input
            v-model="email"
            label="Your Email *"
            type="email"
            dense
            outlined
            :rules="[
              (val) => !!val || 'Email is required.',
              (val) => isValidEmail(val) || 'Enter a valid email.',
            ]"
          />
          <q-input
            v-model="password"
            label="Password *"
            type="password"
            dense
            outlined
            :rules="[(val) => !!val || 'Password is required.']"
          >
            <template v-slot:after>
              <div class="password-strength">
                <span v-if="passwordStrength" :class="strengthClass">{{
                  passwordStrength
                }}</span>
              </div>
            </template>
          </q-input>
          <q-input
            v-model="confirmPassword"
            label="Confirm Password *"
            type="password"
            dense
            outlined
            :rules="[
              (val) => !!val || 'Confirm password is required.',
              (val) => val === password || 'Passwords must match.',
            ]"
          />
          <q-btn type="submit" label="Register" class="register-btn" />
        </q-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed,onMounted } from "vue";
import { useRouter } from "vue-router";

// State variables
const name = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
// Vue Router
const router = useRouter();

// Password strength computation
const passwordStrength = computed(() => {
  if (!password.value) return ""; // No strength displayed for empty password

  const length = password.value.length;
  const hasUppercase = /[A-Z]/.test(password.value);
  const hasNumber = /[0-9]/.test(password.value);
  const hasSpecialChar = /[^a-zA-Z0-9]/.test(password.value);

  const meetsCriteria = hasUppercase && hasNumber && hasSpecialChar;

  // if (!meetsCriteria) return "Weak";
  if (!meetsCriteria || length < 6) return "Weak";
  if (length >= 6 && length <= 12) return "Medium";
  if (length > 12) return "Strong";

  return "Weak";
});

const strengthClass = computed(() => {
  const strength = passwordStrength.value;
  return {
    Weak: "weak",
    Medium: "medium",
    Strong: "strong",
  }[strength];
});

// Redirect to login
const redirectToLogin = () => {
  router.push("/login");
};

// Email validation function
const isValidEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

function handleRegister() {
  console.log("Username:", name.value);
  console.log("Email:", email.value);
  console.log("Password:", password.value);

  // Validate inputs
  if (!name.value || !isValidEmail(email.value) || !password.value) {
    errorMessage.value = "Please fill in all required fields with valid values.";
    console.error("Validation Error:", errorMessage.value);
    return;
  }

  // Create a JSON object for request payload
  const dataObj = {
    username: name.value,
    email: email.value,
    password: password.value,
    role: "user",
  };

  axios
  .post("https://asp-final-project.onrender.com/v1/user/register", dataObj, {
    headers: { "Content-Type": "application/json" },
  })
  .then(function (response) {
    console.log("Register Response:", response.data);

    if (response.data && response.data.user_id) {
      console.log(response.data.message);
      localStorage.setItem("user_id", response.data.user_id);

      router.push("/Login"); // Redirect to login after successful registration
    } else {
      errorMessage.value = "Unexpected response format.";
      console.warn("Unexpected Response Format:", response.data);
    }
  })
  .catch(function (error) {
    console.error("Register Failed:", error.response?.data || error.message);
    errorMessage.value =
      error.response?.data?.message || "Register failed. Please try again.";
  });
}

</script>

<style scoped>
/* Original Styling */
.registration-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  font-family: Arial, sans-serif;
  background: linear-gradient(135deg, #6a0dad, #b19cd9);
  position: relative;
}

.login-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: white;
  color: #6a0dad;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.login-btn:hover {
  color: white;
  background: #6a0dad;
}

.form-layout {
  display: flex;
  width: 90%;
  max-width: 1200px;
  background: white;
  border-radius: 16px 0 0 16px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.left-section {
  flex: 1;
  background: #6a0dad;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 20px;
}

.symbol-container {
  max-width: 200px;
}

.earth-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 20px;
}

.form-section {
  flex: 1.5;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #6a0dad;
  text-align: center;
}

.q-input {
  margin-bottom: 15px;
}

.register-btn {
  width: 100%;
  background-color: #6a0dad;
  color: white;
  border: none;
  padding: 12px;
  font-size: 16px;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 15px;
}

.register-btn:hover {
  background-color: #5e0cb0;
}

/* Password strength indicator */
.password-strength {
  margin-top: 5px;
  font-size: 12px;
}

.password-strength .weak {
  color: red;
}

.password-strength .medium {
  color: orange;
}

.password-strength .strong {
  color: green;
}
</style>
