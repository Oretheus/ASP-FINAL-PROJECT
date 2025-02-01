<template>
  <div class="task-list">
    <h2>Tasks</h2>
    <!-- Filter Dropdown -->
    <div class="filters">
      <label for="filter">Filter Tasks:</label>
      <select id="filter" v-model="filter">
        <option value="All">All</option>
        <option value="Completed">Completed</option>
        <option value="Pending">Pending</option>
      </select>
    </div>

    <!-- Task List -->
    <ul v-if="filteredTasks.length">
      <li v-for="task in filteredTasks" :key="task.id">
        <label>
          <input
            type="checkbox"
            v-model="task.completed"
            @change="completeTask(task)"
          />
          {{ task.description }}
        </label>
        <button class="delete-btn" @click="deleteTask(task.id)">Delete</button>
      </li>
    </ul>
    <p v-else>No tasks available. Add a new task to get started!</p>

    <!-- Add Task Form -->
    <div class="add-task">
      <h3>Add a New Task</h3>
      <form @submit.prevent="addTask">
        <input
          type="text"
          v-model="newTask"
          placeholder="Enter new task description"
          required
        />
        <button type="submit" class="add-btn">Add Task</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: ['tasks'],
  data() {
    return {
      filter: 'All', // Task filter (All, Completed, Pending)
      newTask: '', // Input for the new task description
    };
  },
  computed: {
    filteredTasks() {
      // Filters tasks based on the selected filter
      if (this.filter === 'All') return this.tasks;
      return this.tasks.filter(
        (task) => (this.filter === 'Completed' ? task.completed : !task.completed)
      );
    },
  },
  methods: {
    completeTask(task) {
      // Alerts when a task's completion status changes
      alert(`Task ${task.completed ? 'completed' : 'incomplete'}: ${task.description}`);
    },
    addTask() {
      // Emits an event to add a new task
      const newTaskObject = {
        id: Date.now(), // Unique ID for the new task
        description: this.newTask,
        completed: false,
      };
      this.$emit('add-task', newTaskObject); // Sends new task to the parent
      this.newTask = ''; // Clears the input field
    },
    deleteTask(taskId) {
      // Emits an event to delete a task
      this.$emit('delete-task', taskId);
    },
  },
};
</script>

<style>
.task-list .filters
{
  margin-bottom: 10px;
}

.task-list ul
{
  padding: 0;
  list-style: none;
}

.task-list li
{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0;
}

.add-task
{
  margin-top: 20px;
}

.add-btn,
.delete-btn
{
  background-color: #6a0dad;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn:hover,
.delete-btn:hover 
{
  color:#6a0dad;
  border:solid 1px;
  border-color:#6a0dad;
  background-color: white;
}
</style>
  
  
  