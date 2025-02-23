<template>
  <div class="search-bar">
    <input
      type="text"
      placeholder="Search tasks or applications..."
      v-model="query"
      @input="$emit('search', query)"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
    };
  },
};
</script>

<style>
.search-bar input
{
  width: 98%;
  padding: 10px;
  margin-bottom: 20px;
  font-size: 16px;
  border: 1px solid #6a0dad;
  border-radius: 4px;
  background-color: #f0f8ff;
}

.search-bar input:focus
{
  outline: none;
  border-color: #6a0dad;
}
</style>
