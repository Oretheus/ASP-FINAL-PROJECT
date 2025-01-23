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
          <p>Register here to make the world your oyster</p>
        </div>
      </div>

      <!-- Right Section with Registration Form -->
      <div class="form-section">
        <h2>Register</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <input type="text" v-model="name" placeholder="First Name *" />
            <small v-if="errors.name">{{ errors.name }}</small>
          </div>
          <div class="form-group">
            <input type="email" v-model="email" placeholder="Your Email *" />
            <small v-if="errors.email">{{ errors.email }}</small>
          </div>
          <div class="form-group">
            <input type="password" v-model="password" placeholder="Password *" />
            <small v-if="errors.password">{{ errors.password }}</small>
            <!-- Password Strength Indicator -->
            <div v-if="password" class="password-strength">
              <span :class="strengthClass">{{ passwordStrength }}</span>
            </div>
          </div>
          <div class="form-group">
            <input
              type="password"
              v-model="confirmPassword"
              placeholder="Confirm Password *"
            />
            <small v-if="errors.confirmPassword">{{ errors.confirmPassword }}</small>
          </div>
          <button type="submit" class="register-btn">Register</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Register form data
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      errors: {},
    };
  },

  computed: {
    passwordStrength() {
      if (this.password.length < 6) return 'Weak';
      if (/[A-Z]/.test(this.password) && /[0-9]/.test(this.password)) return 'Medium';
      if (this.password.length >= 8 && /[A-Z]/.test(this.password) && /[0-9]/.test(this.password) && /[^a-zA-Z0-9]/.test(this.password)) {
        return 'Strong';
      }
      return 'Weak';
    },
    strengthClass() {
      const strength = this.passwordStrength;
      return {
        'weak': strength === 'Weak',
        'medium': strength === 'Medium',
        'strong': strength === 'Strong',
      };
    },
  },

  methods: {
    redirectToLogin() {
      this.$router.push('/login'); // Redirect to Login page
    },
    handleRegister() {
      this.errors = {};
      if (!this.name) this.errors.name = 'Name is required.';
      if (!this.email || !/\S+@\S+\.\S+/.test(this.email)) this.errors.email = 'Valid email is required.';
      if (!this.password) this.errors.password = 'Password is required.';
      if (this.password !== this.confirmPassword)
        this.errors.confirmPassword = 'Passwords do not match.';
      if (Object.keys(this.errors).length === 0) {
        alert('Registration successful!');
      }
    },
  },
};
</script>

<style scoped>
/* General Layout */
.registration-container {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Center vertically */
  align-items: center; /* Center horizontally */
  min-height: 100vh; /* Full height */
  background: linear-gradient(135deg, #6a0dad, #b19cd9); /* Purple to lilac gradient */
  font-family: Arial, sans-serif;
  position: relative;
  padding: 20px;
}

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

/* Redirect Button */
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
  background: #f3f3f3;
}

/* Form Layout */
.form-layout {
  display: flex;
  width: 90%;
  max-width: 1200px;
  height: auto;
  background: white;
  border-radius: 16px 0 0 16px; /* Rounded left side */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  align-items: center; /* Center vertically */
}

/* Left Section */
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

.symbol-container p {
  font-size: 18px;
  font-weight: bold;
  line-height: 1.5;
}

/* Right Section */
.form-section {
  flex: 1.5;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center; /* Center vertically */
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #6a0dad;
  text-align: center;
}

.form-group {
  margin-bottom: 15px;
}

input {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #6a0dad;
  box-shadow: 0 0 5px rgba(106, 13, 173, 0.5);
}

small {
  color: red;
  font-size: 12px;
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
</style>
