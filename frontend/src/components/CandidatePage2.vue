<template>
  <q-layout>
    <q-header
      elevated
      class="q-py-sm"
      :style="{
        background: 'linear-gradient(135deg, #286ea6, #1a4d80)',
        height: '65px',
        borderBottom: '2px solid #1a4d80',
      }"
    >
      <q-toolbar class="q-pa-none">
        <q-avatar size="40px" class="q-ml-md">
          <img src="@/assets/earth.png" alt="Logo" class="earth-icon" />
        </q-avatar>

        <q-space />

        <q-tabs align="right" class="q-mr-md">
          <q-route-tab to="/candidate1">
            <q-icon name="home" size="30px" />
          </q-route-tab>

          <q-route-tab to="/candidate2" icon="task" />
        </q-tabs>
      </q-toolbar>
    </q-header>
    <div class="candidate-container">
      <q-btn
        label="Back to Candidate Page 1"
        @click="goToCandidatePage1"
        class="q-mt-md"
        style="background-color: #6a0dad; color: white"
      />

      <!-- Search Bar for Applications -->
      <div class="search-section">
        <SearchBar
          @search="searchQuery = $event"
          placeholder="Search applications..."
        />
      </div>

      <div class="main-sections">
        <!-- Applications Section -->
        <div class="section application-status-section">
          <h4>Application Status</h4>

          <p v-if="applications.length === 0">No applications found.</p>

          <q-table
            v-if="filteredApplications.length > 0"
            class="styled-table"
            :rows="filteredApplications"
            :columns="columns"
            row-key="application_id"
            virtual-scroll
            :style="{
              backgroundColor: collectionStore.darkMode ? '#858282' : '#ffffff',
            }"
          >
            <template v-slot:body="props">
              <q-tr :props="props">
                <q-td key="status">{{ props.row.status }}</q-td>
                <q-td key="job_title">{{ props.row.job_title }}</q-td>
                <q-td key="company_name">{{ props.row.company_name }}</q-td>
              </q-tr>
            </template>
          </q-table>

          <p v-else>No results match your search.</p>
        </div>

        <!-- Tasks Section (Using TaskListWithFilters Component) -->
        <div class="section task-list-section">
          <!-- <h2>Task Manager</h2> -->

          <TaskListWithFilters
            :tasks="tasks"
            @add-task="addTask"
            @delete-task="deleteTask"
            @toggle-task="toggleTaskCompletion"
            @search="searchTaskQuery = $event"
          />
        </div>
      </div>
    </div>
  </q-layout>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, computed, onMounted, watch } from "vue";
import axios from "axios";
import SearchBar from "./CandidatePageComponents/SearchBar.vue";
import ApplicationStatus from "./CandidatePageComponents/ApplicationStatus.vue";
import TaskListWithFilters from "./CandidatePageComponents/TaskListWithFilters.vue";
import { useCollectionStore } from "@/stores/mycore";
// State variables
const loading = ref(true);
const errorMessage = ref("");
const searchQuery = ref("");
const applications = ref([]);
const searchTaskQuery = ref(""); // For Task Manager Filtering
const tasks = ref([]);
const user_id = ref(localStorage.getItem("user_id") || null); // Store logged-in user ID
const router = useRouter();

const collectionStore = useCollectionStore();

const goToCandidatePage1 = () => {
  router.push("/candidate1"); // Adjust the route if needed
};
const columns = [
  { name: "status", label: "Status", field: "status", align: "left" },
  { name: "job_title", label: "Job Title", field: "job_title", align: "left" },
  { name: "company_name", label: "Company Name", field: "company_name", align: "left" },
];

const fetchApplications = async () => {
  const token = localStorage.getItem("authToken"); // Get token from localStorage
  const userId = localStorage.getItem("user_id"); // Get user ID

  console.log("🔹 Stored Token Before Request:", token);
  console.log("🔹 Stored User ID Before Request:", userId);

  if (!token || !userId) {
    console.error(" Missing Token or User ID! API request cannot be made.");
    errorMessage.value = "Authentication error. Please log in again.";
    loading.value = false;
    return;
  }

  try {
    const response = await axios.get(
      `https://asp-final-project.onrender.com/v1/application/user/${userId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`, // Include token in headers
          "Content-Type": "application/json",
        },
      }
    );

    console.log("✅ API Response:", response.data);

    // Ensure correct data mapping
    applications.value = response.data.map((app) => ({
      status: app.status,
      job_title: extractJobTitle(app.job_id),
      company_name: extractCompanyName(app.job_id),
    }));
  } catch (error) {
    console.error(" API Fetch Failed:", error.response?.data || error.message);
    errorMessage.value =
      error.response?.data?.message || "Failed to fetch applications.";
  } finally {
    loading.value = false;
  }
};

// Extract job title and company name from encoded job_id
const extractJobTitle = (encodedJobId) => {
  try {
    const decoded = JSON.parse(atob(encodedJobId));
    return decoded.job_title || "Unknown Job Title";
  } catch {
    return "Unknown Job Title";
  }
};

const extractCompanyName = (encodedJobId) => {
  try {
    const decoded = JSON.parse(atob(encodedJobId));
    return decoded.company_name || "Unknown Company";
  } catch {
    return "Unknown Company";
  }
};

//  Fetch user ID & data when component loads
onMounted(async () => {
  console.log("🔹 CandidatePage2 is mounted!");
  user_id.value = localStorage.getItem("user_id") || null;
  console.log("🔹 Retrieved user_id:", user_id.value);

  if (user_id.value) {
    await fetchApplications();
    console.log("✅ Applications fetched:", applications.value);
  } else {
    console.warn("⚠️ No user_id found. Applications will not load.");
  }
});

/// ✅ Filter Applications (Live Search)
const filteredApplications = computed(() => {
  return applications.value.filter((app) => {
    const query = searchQuery.value.toLowerCase();
    return (
      app.job_title.toLowerCase().includes(query) ||
      app.company_name.toLowerCase().includes(query) ||
      app.status.toLowerCase().includes(query)
    );
  });
});

// Save tasks to LocalStorage whenever they change
watch(
  tasks,
  (newTasks) => {
    localStorage.setItem("tasks", JSON.stringify(newTasks));
  },
  { deep: true }
);

// ✅ Task Functions
const addTask = (task) => {
  tasks.value.push({ id: Date.now(), ...task, completed: false });
};

const deleteTask = (taskId) => {
  tasks.value = tasks.value.filter((task) => task.id !== taskId);
};

const toggleTaskCompletion = (taskId) => {
  const task = tasks.value.find((t) => t.id === taskId);
  if (task) {
    task.completed = !task.completed;
  }
};
</script>

 <style scoped>
/* General Layout */
.candidate-container {
  width: 90%;
  margin: auto;
  font-family: Arial, sans-serif;
}

/* Search Section */
.search-section {
  margin-top: 100px;
  margin-bottom: 15px;
}

/* Table Styling */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.styled-table th,
.styled-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

/* Sections */
.main-sections {
  display: flex;
  justify-content: space-between;
}

.application-status-section {
  width: 60%;
}

.task-list-section {
  width: 35%;
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
}

/* Task Manager */
.task-input {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.task-input input {
  padding: 5px;
  border: 1px solid #ccc;
}

.task-input button {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.task-list-section ul {
  list-style: none;
  padding: 0;
}

.task-list-section li {
  display: flex;
  justify-content: space-between;
  background: white;
  padding: 5px;
  margin-bottom: 5px;
  border-radius: 3px;
}

.task-list-section button {
  background: red;
  color: white;
  border: none;
  padding: 5px;
  cursor: pointer;
}
</style>
