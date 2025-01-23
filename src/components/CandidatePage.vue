<template>
  <div id="app">
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

<script>
import { onMounted, ref, computed } from 'vue';
import SearchBar from './CandidatePageComponents/SearchBar.vue'; 
import ApplicationStatus from './CandidatePageComponents/ApplicationStatus.vue'; 
import TaskListWithFilters from './CandidatePageComponents/TaskListWithFilters.vue'; 
import { fetchApplications } from '../services/api.js'; // Mock API

export default {
  components: {
    SearchBar,
    ApplicationStatus,
    TaskListWithFilters,
  },
  setup() {
    // State variables
    const searchQuery = ref('');
    const applications = ref([]);
    const tasks = ref([]); // Tasks start as an empty array

    // Fetch Applications Data (e.g., from API or mock service)
    const fetchData = async () => {
      applications.value = await fetchApplications(); // Fetch applications dynamically
    };

    onMounted(fetchData);

    // Computed: Filter applications based on the search query
    const filteredApplications = computed(() =>
      applications.value.filter((app) =>
        app.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    );

    // Computed: Filter tasks based on the search query
    const filteredTasks = computed(() =>
      tasks.value.filter((task) =>
        task.description.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    );

    // Methods
    const handleSearch = (query) => {
      searchQuery.value = query; // Update the search query for both tasks and applications
    };

    const addTask = (newTask) => {
      tasks.value.push(newTask); // Add new task to the tasks array
    };

    const deleteTask = (taskId) => {
      tasks.value = tasks.value.filter((task) => task.id !== taskId); // Remove task by ID
    };

    // Return to template
    return {
      searchQuery,
      applications,
      tasks,
      filteredApplications,
      filteredTasks,
      handleSearch,
      addTask,
      deleteTask,
    };
  },
};
</script>

<style scoped>
/* Page Styles */
#app {
  font-family: 'Arial', sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f8faff;
  border: 1px solid #e1e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.app-header {
  background: linear-gradient(135deg, #6a0dad, #b19cd9);
  color: white;
  padding: 20px;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  /* border-bottom: 4px solid #0056b3; */
}

.content {
  padding: 20px;
}

.main-sections {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.section {
  flex: 1;
  background-color: white;
  border: 1px solid #e1e8f0;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>

  