<template>
  <q-layout>
    <q-header
      elevated
      class="q-py-sm"
      :style="{ background: '#286ea6', height: '56px' }"
    >
      <q-toolbar class="q-pa-none">
        <q-avatar size="40px" class="q-ml-md">
          <img src="@/assets/earth.png" alt="Logo" class="earth-icon" />
        </q-avatar>

        <q-space />

        <q-tabs align="right" class="q-mr-md">
          <q-route-tab to="/" icon="home" />
          <q-route-tab to="/candidate2" icon="task" />
        </q-tabs>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="q-pa-md">
        <div class="row q-gutter-md justify-center">
          <!-- Points & Streak Card -->
          <q-card class="dashboard-card shadow-3">
            <q-card-section class="text-center">
              <q-icon name="emoji_events" size="50px" color="amber" />
              <div class="text-h6 text-bold q-mt-md">Your Points</div>
              <div class="text-h6 text-primary q-mt-sm">{{ points }}</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="q-gutter-md flex justify-center" style="width: 100%">
          <q-card
            class="q-pa-md q-mb-xl q-mt-xl"
            style="
              width: 600px;
              max-width: 100%;
              box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            "
            bordered
          >
            <div class="q-gutter-md">
              <!-- Job Title Input -->
              <q-input
                v-model="searchQuery"
                label="Job Title"
                outlined
                dense
                class="q-mb-sm"
                placeholder="Enter job title"
              />

              <!-- Location Input -->
              <q-input
                v-model="searchLocation"
                label="Location"
                outlined
                dense
                class="q-mb-sm"
                placeholder="Enter location"
              />

              <!-- Search Button -->
              <div class="q-mt-md flex justify-center">
                <q-btn
                  @click="searchJobs"
                  label="Search"
                  icon="search"
                  :style="{
                    borderColor: '#97b5e6',
                    backgroundColor: '#afd5fa',
                    width: '55%',
                  }"
                />
              </div>
            </div>
          </q-card>
        </div>

        <div class="q-gutter-md flex justify-center">
          <!-- Job Listings Card -->
          <q-card class="my-card q-pa-md q-mx-xl" style="width: 40%">
            <q-card-section>
              <div class="text-center">
                <q-item-label class="text-h6 q-mb-lg"
                  >Job Listings</q-item-label
                >
              </div>
              <q-scroll-area style="height: 500px; max-width: 600px">
                <div v-for="(job, index) in jobs" :key="index">
                  <q-item>
                    <!-- Main job details -->
                    <q-item-section>
                      <q-item-label class="text-subtitle2">{{
                        job.job_title
                      }}</q-item-label>
                      <q-item-label caption
                        >{{ job.company_name }} -
                        {{ job.address_city }}</q-item-label
                      >
                    </q-item-section>

                    <!-- Right-aligned buttons -->
                    <q-item-section side>
                      <div class="row items-center">
                        <!-- Favourite Button -->
                        <q-btn
                          flat
                          round
                          color="red"
                          icon="favorite"
                          @click="saveJob(job.jobId)"
                          class="q-mr-md"
                        />

                        <div>
                          <!-- Apply Button -->
                          <q-btn
                            color="#f8a200"
                            label="Details"
                            @click="getJobDetails(job.jobId)"
                            :style="{
                              borderColor: '#97b5e6',
                              backgroundColor: '#afd5fa',
                            }"
                            class="text-black q-mr-md"
                          />
                        </div>
                      </div>
                    </q-item-section>
                  </q-item>
                  <q-separator class="q-my-md" />
                </div>
              </q-scroll-area>
            </q-card-section>
            <!-- Load More Button -->
            <q-btn
              v-if="nextPageToken"
              @click="loadMoreJobs"
              class="q-mt-md"
              :style="{
                borderColor: '#97b5e6',
                borderRadius: '1000px',
              }"
              stack
            >
              <q-icon name="expand_more" size="20px" />
            </q-btn>
          </q-card>

          <!-- Favorites Card -->
          <q-card class="my-card q-pa-md" style="width: 40%">
            <q-card-section>
              <div class="text-center">
                <q-item-label class="text-h6 q-mb-lg">Favourites</q-item-label>
              </div>

              <q-scroll-area style="height: 500px; max-width: 600px">
                <div v-for="(job, index) in favouritesList" :key="index">
                  <q-item>
                    <q-item-section>
                      <!-- Main job details -->
                      <q-item-label class="text-subtitle2">{{
                        job.job.title
                      }}</q-item-label>
                      <q-item-label caption>
                        {{ job.job.company_name }}
                      </q-item-label>
                    </q-item-section>

                    <!-- Right-aligned buttons -->
                    <q-item-section side>
                      <div class="row items-center">
                        <!-- Favourite Button -->
                        <q-btn
                          flat
                          round
                          color="black"
                          icon="delete"
                          @click="deleteJob(job.job.application_id)"
                          class="q-mr-md"
                        />

                        <div>
                          <!-- Apply Button -->
                          <q-btn
                            color="#f8a200"
                            label="Details"
                            @click="getJobDetails(job.job.job_id)"
                            :style="{
                              borderColor: '#97b5e6',
                              backgroundColor: '#afd5fa',
                            }"
                            class="text-black q-mr-sm"
                          />
                        </div>
                      </div>
                    </q-item-section>
                  </q-item>
                  <q-separator class="q-my-md" />
                </div>
              </q-scroll-area>
            </q-card-section>
          </q-card>
        </div>

        <!-- Job Details Dialog -->

        <q-scroll-area style="height: 500px; max-width: 80vw">
          <q-dialog v-model="dialogVisible" class="bg-light-grey">
            <q-card
              class="q-mt-none q-pa-md"
              style="max-width: 80vw; width: 600px"
            >
              <q-card-section>
                <div class="text-h6 text-center q-mb-lg">JOB DETAILS</div>
                <div
                  class="bg-blue-1 q-pa-sm q-mt-xs"
                  style="border-radius: 8px"
                >
                  <div>
                    <strong>Job Title:</strong>
                    {{ jobDetails.job_details.title }}
                  </div>
                  <div>
                    <strong>Company:</strong>
                    {{ jobDetails.job_details.company_name }}
                  </div>
                  <div>
                    <strong>Location:</strong>
                    {{ jobDetails.job_details.location }}
                  </div>
                </div>

                <div class="q-mt-md">
                  <strong>Description:</strong>
                </div>
                <div
                  class="bg-blue-1 q-pa-sm q-mt-xs"
                  style="border-radius: 8px"
                >
                  <q-scroll-area style="height: 100px; max-width: 100%">
                    <p class="q-mb-md">
                      {{ jobDetails.job_details.description }}
                    </p>
                  </q-scroll-area>
                </div>

                <div class="q-mt-md"><strong>Apply Options:</strong></div>

                <q-list bordered separator>
                  <q-item
                    v-for="option in jobDetails.job_details.apply_options"
                    :key="option.link"
                    clickable
                    tag="a"
                    :href="option.link"
                    target="_blank"
                  >
                    <q-item-section>{{ option.title }}</q-item-section>
                  </q-item>
                </q-list>

                <div class="q-mt-md">
                  <q-btn
                    outline
                    color="primary"
                    label="View Job Posting"
                    :href="jobDetails.job_details.share_link"
                    target="_blank"
                  />
                </div>
              </q-card-section>

              <q-card-actions align="right">
                <q-btn
                  flat
                  color="red"
                  label="Close"
                  @click="dialogVisible = false"
                />
              </q-card-actions>
            </q-card>
          </q-dialog>
        </q-scroll-area>
      </q-page>
    </q-page-container>
  </q-layout>
  {{ savedJobs }}
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const searchQuery = ref("Software developer remote");
const searchLocation = ref("toronto");
const jobs = ref([]);
const jobIds = ref([]);
const nextPageToken = ref(null);
const favourites = ref(JSON.parse(localStorage.getItem("favourites")) || []);
const selectedJob = ref(null);
const dialogVisible = ref(false);
const jobDetails = ref({});
const savedJobs = ref({});
const favouritesList = ref([]);
const points = ref(0);
const streak = ref(0);

const decodeBase64Results = (results) => {
  return results.map((result) => {
    const decoded = JSON.parse(atob(result));
    return decoded;
  });
};

//searchJobs
const searchJobs = async () => {
  const payload = {
    query: searchQuery.value,
    location: searchLocation.value,
  };

  console.log("Payload being sent:", JSON.stringify(payload, null, 2));

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.error("Authorization token is missing!");
      return;
    }
    console.log("Stored Token:", token);

    const response = await axios.post(
      "https://asp-final-project.onrender.com/v1/search/jobs",
      payload,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    console.log("API Response:", response.data);

    // Check if the message indicates a successful search
    if (
      response.data.message ===
      "Initial Search - Search results retrieved successfully."
    ) {
      if (response.data.results && response.data.results.length > 0) {
        console.log("response.data.results:", response.data.results);
        jobIds.value = response.data.results;
        console.log("jobIds.value:", jobIds.value);
        // Decode the job results if needed
        const decodedJobs = decodeBase64Results(response.data.results);
        if (jobIds.value.length === decodedJobs.length) {
          jobs.value = decodedJobs.map((job, index) => {
            const jobWithId = {
              ...job,
              jobId: jobIds.value[index], // Assign the specific job's ID from jobIds
            };
            console.log(`Job at index ${index}:`, jobWithId); // Debugging log to check each job's ID
            return jobWithId;
          });

          console.log("Final Jobs Array:", jobs.value);
        } else {
          console.error("Mismatch in length between jobIds and decodedJobs");
        }

        nextPageToken.value = response.data.next_page_token || null;
        console.log("nextPageToken.value:", nextPageToken.value);
        const searchId = response.data.search_id || null;
        if (searchId) {
          localStorage.setItem("search_id", searchId); // Store search_id
        }
        console.log("Jobs retrieved:", jobs.value);
      } else {
        console.warn("No jobs found for your search.");
      }
    } else {
      console.error(
        "Failed to retrieve jobs:",
        response.data.message || "Unknown error."
      );
    }
  } catch (error) {
    console.error(
      "Error searching for jobs:",
      error.response?.data || error.message
    );
  }
};

//loadMoreJobs
const loadMoreJobs = async () => {
  const searchId = localStorage.getItem("search_id");
  const token = localStorage.getItem("authToken");

  if (searchId) {
    try {
      const response = await axios.post(
        "https://asp-final-project.onrender.com/v1/search/jobs",
        {
          search_id: searchId,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.data.message) {
        const decodedJobs = decodeBase64Results(response.data.results);
        jobs.value = [...jobs.value, ...decodedJobs]; //appending
        console.log(response.data.message);
        console.log("Additional jobs retrived:", response.data);
      } else {
        console.log("No more results.");
      }
    } catch (error) {
      console.error("Error loading more jobs:", error);
    }
  } else {
    console.error("Search ID is missing or expired.");
  }
};

//saveJob

const saveJob = async (jobId) => {
  const token = localStorage.getItem("authToken");

  try {
    // Save the job
    const response = await axios.post(
      `https://asp-final-project.onrender.com/v1/application/save/${jobId}`,
      {},
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    console.log("Job saved successfully:", response.data);

    // Extract application_id 
    const applicationId = response.data.application_id;
    if (!applicationId) {
      throw new Error("No application_id found in the response");
    }
    points.value = 0;
    points.value = response.data.points.total_points;
    // console.log("points.value:", points.value);
    // Fetch application details using the application_id
    const savedJobDetails = await axios.get(
      `https://asp-final-project.onrender.com/v1/application/details/${applicationId}`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    // console.log("Application details:", savedJobDetails.data);
    savedJobs.value = savedJobDetails.data;
    console.log("savedJobs.value:", savedJobs.value);
    favouritesList.value.push(savedJobs.value);
    console.log("favouritesList.value:", favouritesList.value);
  } catch (error) {
    console.error("Error:", error.response?.data || error.message);
    throw error;
  }
};

//fetchPoints
const fetchPoints = async () => {
  const token = localStorage.getItem("authToken");
 
  try {
    const response = await axios.get(
      `https://asp-final-project.onrender.com/v1/user/points`,

      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    points.value = 0;
    points.value = response.data.current_points || 0;
  } catch (error) {
    console.error("Error fetching points:", error);
  }
};

//fetchAllApplications
const fetchAllApplications = async () => {
  const token = localStorage.getItem("authToken"); 
  const userId = localStorage.getItem("user_id"); // Retrieve the user_id

  if (!userId) {
    console.error("User ID not found in localStorage.");
    return;
  }

  try {
    const response = await axios.get(
      `https://asp-final-project.onrender.com/v1/application/user/${userId}`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // Include auth token for authorization
        },
      }
    );

    console.log("Applications Fetched:", response.data);
    return response.data; // Return data for further use
  } catch (error) {
    console.error("Error fetching applications:", error.response?.data || error.message);
  }
};

//getting job details
const getJobDetails = async (jobId) => {
  const token = localStorage.getItem("authToken");
  console.log("jobId:", jobId);
  if (!token) {
    console.error("Authorization token is missing.");
    return;
  }

  try {
    const response = await axios.get(
      `https://asp-final-project.onrender.com/v1/search/job/${jobId}`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    console.log("Job details response:", response.data);

    if (response.data) {
      jobDetails.value = response.data;
      dialogVisible.value = true; // Show job details dialog
    } else {
      console.warn("No job details found.");
    }
  } catch (error) {
    console.error(
      "Error fetching job details:",
      error.response?.data || error.message
    );
  }
};

const deleteJob = async (applicationId) => {
  const token = localStorage.getItem("authToken");
  console.log("applicationId:", applicationId);
  if (!token) {
    console.error("Authorization token is missing.");
    return;
  }

  try {
    const response = await axios.get(
      `https://asp-final-project.onrender.com/v1/application/delete/${applicationId}`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    console.log("Job deletion response:", response.data);

    if (response.data) {
      console.log("Job deleted successfully:", response.data);

      // Fetch application details using the application_id
      const savedJobDetails = await axios.get(
        `https://asp-final-project.onrender.com/v1/application/details/${applicationId}`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      savedJobs.value = {};
      savedJobs.value = savedJobDetails.data;
      console.log("savedJobs.value:", savedJobs.value);
    } else {
      console.warn("No response data after deletion.");
    }
  } catch (error) {
    console.error("Error deleting job:", error.response?.data || error.message);
  }
};

onMounted(() => {
  fetchPoints();
  // fetchLeaderboard();
  fetchAllApplications();
});
</script>

<style scoped>
.q-card {
  border-radius: 20px;
  overflow: hidden;
  background-color: white;
}
.my-card {
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.4);
}
.bg-light-grey {
  background-color: #f5f5f5 !important;
}

.q-card .q-card-section {
  font-size: 16px;
}
/* Dashboard Card */
.dashboard-card {
  width: 1900px;
  height: 200px;
  max-width: 100%;
  padding: 20px;
  border-radius: 15px;
  background-color: #ebf3fb !important;
}

/* Leaderboard Card */
.leaderboard-card {
  width: 450px;
  max-width: 100%;
  padding: 20px;
  border-radius: 15px;
  background-color: #f8f9fa;
}
</style>
