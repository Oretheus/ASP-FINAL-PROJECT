<template>
  <q-card class="q-pa-md">
    <q-card-section>
      <h4>Tasks</h4>

      <!-- Filter Dropdown -->
      <div class="q-mb-md">
        <q-select
          label="Filter Tasks"
          v-model="filter"
          :options="filterOptions"
          outlined
          dense
        />
      </div>

      <!-- Task List -->
      <q-list v-if="filteredTasks.length" bordered separator>
        <q-item v-for="task in filteredTasks" :key="task.id">
          <q-item-section avatar>
            <q-checkbox v-model="task.completed" @update:model-value="completeTask(task)" />
          </q-item-section>
          <q-item-section>{{ task.description }}</q-item-section>
          <q-item-section side>
            <q-btn flat color="red" icon="delete" @click="deleteTask(task.id)" />
          </q-item-section>
        </q-item>
      </q-list>

      <q-banner v-else class="text-grey">
        No tasks available. Add a new task to get started!
      </q-banner>
    </q-card-section>

    <!-- Add Task Form -->
    <q-separator />

    <q-card-section>
      <h5>Add a New Task</h5>
      <q-form @submit.prevent="addTask">
        <q-input v-model="newTask" label="Enter new task description" outlined dense required />
        <q-btn type="submit" color="primary" label="Add Task" class="q-mt-md" />
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script setup>
import { defineProps, defineEmits, ref, computed } from "vue";
import { useQuasar } from "quasar";

const props = defineProps({
  tasks: Array,
});

const emit = defineEmits(["add-task", "delete-task"]);

const $q = useQuasar();
const filter = ref("All");
const newTask = ref("");
const filterOptions = ["All", "Completed", "Pending"];

const filteredTasks = computed(() => {
  if (filter.value === "All") return props.tasks;
  return props.tasks.filter((task) => (filter.value === "Completed" ? task.completed : !task.completed));
});

const completeTask = (task) => {
  $q.notify({
    message: `Task ${task.completed ? "completed" : "marked incomplete"}: ${task.description}`,
    color: task.completed ? "green" : "orange",
    position: "top",
  });
};

const addTask = () => {
  if (!newTask.value.trim()) return;

  const newTaskObject = {
    id: Date.now(),
    description: newTask.value,
    completed: false,
  };
  emit("add-task", newTaskObject);
  newTask.value = "";
};

const deleteTask = (taskId) => {
  emit("delete-task", taskId);
};
</script>

<style scoped>
.q-card {
  max-width: 500px;
  margin: auto;
}
</style>
