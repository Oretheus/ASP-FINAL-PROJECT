<template>
    <div class="application-status">
      <h2>Application Status</h2>
      <table>
        <thead>
          <tr>
            <th>Job Title</th>
            <th>Status</th>
            <th>Deadline</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.title }}</td>
            <td>{{ app.status }}</td>
            <td>{{ app.deadline }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    props: ['applications'],
  };
  </script>
  
  <style>
  .application-status table
  {
    width: 100%;
    border-collapse: collapse;
  }

  .application-status th,
  .application-status td
  {
    border: 1px solid #ddd;
    padding: 8px;
  }
  </style>
  
  
