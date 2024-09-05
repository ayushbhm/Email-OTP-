<template>
    <div class="login-container">
     <h2>User Login</h2>
     

     <!-- Email Input Form -->
    <div>
        <input v-model="email" placeholder="Enter your email">
        <button @click="sendOtp" :disabled="otpSent">Send OTP</button>
    </div>
      

<!-- OTP Verification Form -->

<div v-if="otpSent">
    <input v-model="otp" placeholder="Enter OTP ">
    <button @click="verifyOtp">Verify OTP</button>
</div>
<p>{{ message }}</p>
    </div>
</template>
<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const email = ref(''); // Email input state
    const otp = ref('');   // OTP input state
    const message = ref(''); // Message for success/error feedback
    const otpSent = ref(false); // Boolean to control OTP input visibility

    // Function to send OTP
    const sendOtp = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/send-otp', { email: email.value });
        message.value = response.data.message;
        otpSent.value = true; // Show OTP input after sending
      } catch (error) {
        message.value = 'Error sending OTP';
      }
    };

    // Function to verify OTP
    const verifyOtp = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/verify-otp', { 
          email: email.value, 
          otp: otp.value 
        });
        message.value = response.data.message;
        if (response.data.message === 'OTP verified successfully!') {
          // Handle successful login here (e.g., redirect to dashboard)
          console.log('Login successful!');
        }
      } catch (error) {
        message.value = error.response?.data?.message || 'Error verifying OTP';
      }
    };

    return { email, otp, message, otpSent, sendOtp, verifyOtp };
  }
};
</script>
<style scoped>
/* Add some basic styles for simplicity */
input {
  display: block;
  margin: 10px 0;
  padding: 8px;
}
button {
  padding: 8px 16px;
}
</style>
