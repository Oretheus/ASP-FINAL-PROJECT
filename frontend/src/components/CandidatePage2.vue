<template>
  <div class="candidate-container">
    <!-- Header -->
    <header class="app-header">
      <h1>Candidate Application and Task Tracking</h1>
    </header>

    <!-- Content -->
    <div class="content">
      <!-- Search Bar -->
      <SearchBar @search="handleSearch" />

      <!-- Main Sections -->
      <div class="main-sections">
        <!-- Applications Section -->
        <div class="section application-status-section">
          <ApplicationStatus :applications="filteredApplications" />
        </div>

        <!-- Tasks Section -->
        <div class="section task-list-section">
          <TaskListWithFilters
            :tasks="filteredTasks"
            @add-task="addTask"
            @delete-task="deleteTask"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import SearchBar from "./CandidatePageComponents/SearchBar.vue";
import ApplicationStatus from "./CandidatePageComponents/ApplicationStatus.vue";
import TaskListWithFilters from "./CandidatePageComponents/TaskListWithFilters.vue";
import { fetchApplications } from "../services/api.js";

// State variables
const searchQuery = ref("");
const applications = ref([]);
const tasks = ref([]);

// Fetch applications and tasks
const fetchData = async () => {
  applications.value = await fetchApplications();
};

onMounted(fetchData);

// Computed properties for filtering
const filteredApplications = computed(() =>
  applications.value.filter((app) =>
    app.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

const filteredTasks = computed(() =>
  tasks.value.filter((task) =>
    task.description.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

// Handlers
const handleSearch = (query) => {
  searchQuery.value = query;
};

const addTask = (newTask) => {
  tasks.value.push(newTask);
};

const deleteTask = (taskId) => {
  tasks.value = tasks.value.filter((task) => task.id !== taskId);
};
</script>

<style scoped>

/* General Layout */
.candidate-container
{
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, sans-serif;
  background: #f8faff;
  padding: 20px;
}

.app-header
{
  background: linear-gradient(135deg, #6a0dad, #b19cd9);
  color: white;
  padding: 20px;
  text-align: center;
  font-size: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.content
{
  width: 100%;
  max-width: 1200px;
  padding: 20px;
  background: white;
  border: 1px solid #e1e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.main-sections
{
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.section
{
  flex: 1;
  background-color: white;
  border: 1px solid #e1e8f0;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>