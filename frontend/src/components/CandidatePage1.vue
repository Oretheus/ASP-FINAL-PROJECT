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
          <q-route-tab to="/">
            <q-icon name="home" size="30px" />
          </q-route-tab>

          <q-route-tab to="/candidate2" icon="task" />
        </q-tabs>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="q-pa-md">
        <div class="row q-gutter-md justify-center">
          <q-card
            class="q-pa-md shadow-3"
            :style="{
              width: '1900px',
              height: '200px',
              maxWidth: '100%',
              padding: '20px',
              borderRadius: '15px',
              backgroundColor: collectionStore.darkMode ? '#424242' : '#ebf3fb',
            }"
          >
            <!-- Flex container for both sections -->
            <div
              class="q-gutter-md column"
              style="display: flex; flex-direction: column; align-items: center"
            >
              <!-- Emoji and Points Section: Centered -->
              <div
                style="
                  display: flex;
                  flex-direction: column;
                  align-items: center;
                "
              >
                <q-icon name="emoji_events" size="50px" color="amber" />
                <div class="row q-mt-md">
                  <div class="text-h6 text-bold" style="margin-right: 8px">
                    Your Points:
                  </div>
                  <div class="text-h6 text-primary">{{ points }}</div>
                </div>
              </div>

              <!-- Description Section -->
              <div>
                <p class="text-subtitle2">
                  Points are awarded based on your activity, such as completing
                  tasks, applying for jobs, and reaching milestones. <br />Keep
                  earning points to unlock rewards, gain recognition, and stay
                  motivated in your internship search journey.
                </p>
              </div>
            </div>
          </q-card>
        </div>
        <div class="q-gutter-md flex justify-center" style="width: 100%">
          <q-card
            class="q-pa-md q-mb-xl q-mt-xl"
            style="
              width: 1000px;
              max-width: 100%;
              box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
              margin-top: 100px;
              border-radius: 20px;
              overflow: hidden;
            "
            bordered
          >
            <div class="q-mb-lg text-center">
              <p class="text-h6">Search for Jobs</p>
              <p class="text-subtitle2">
                Enter a job title and location to search for available job
                opportunities. <br />
                You can use the filters to refine your search and find jobs that
                match your skills and preferences.
              </p>
            </div>
            <div class="q-gutter-md">
              <!-- Job Title Input -->
              <q-input
                v-model="searchQuery"
                label="Job Title"
                outlined
                dense
                class="q-mb-sm search-input"
                placeholder="Enter job title"
              />

              <!-- Location Input -->
              <q-input
                v-model="searchLocation"
                label="Location"
                outlined
                dense
                class="q-mb-sm search-input"
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
          <q-card class="job-card q-pa-md q-mx-xl" style="width: 40%">
            <q-card-section>
              <div class="text-center">
                <q-item-label class="text-h6 q-mb-lg"
                  ><b>Job Listings</b></q-item-label
                >
              </div>
              <q-scroll-area style="height: 500px; max-width: 700px">
                <div v-for="(job, index) in jobs" :key="index">
                  <q-item clickable>
                    <!-- Main job details -->
                    <q-avatar square size="50px">
                      <q-icon
                        name="account_circle"
                        size="50px"
                        :style="{ color: '#3678b3' }"
                      />
                    </q-avatar>

                    <q-item-section>
                      <q-item-label class="q-ml-md text-subtitle2">{{
                        job.job_title
                      }}</q-item-label>
                      <q-item-label class="q-ml-md" caption
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
          <q-card class="job-card q-pa-md" style="width: 40%">
            <q-card-section>
              <div class="text-center">
                <q-item-label class="text-h6 q-mb-lg"
                  ><b>Favourites</b></q-item-label
                >
              </div>

              <q-scroll-area style="height: 500px; max-width: 700px">
                <div v-for="(job, index) in favouritesList" :key="index">
                  <q-item clickable>
                    <q-avatar square size="50px">
                      <q-icon
                        name="account_circle"
                        size="50px"
                        :style="{ color: '#3678b3' }"
                      />
                    </q-avatar>
                    <q-item-section>
                      <!-- Main job details -->
                      <q-item-label class="text-subtitle2 q-ml-md">{{
                        job.job.title
                      }}</q-item-label>
                      <q-item-label class="q-ml-md" caption>
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
                          @click="deleteJob(job.application.application_id)"
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
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import _ from "lodash";

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
import { useCollectionStore } from "@/stores/mycore";
const collectionStore = useCollectionStore();

const decodeBase64Results = (results) => {
  return results.map((result) => {
    const decoded = JSON.parse(atob(result));
    return decoded;
  });
};

// Search for jobs based on query and location
const searchJobs = async () => {
  const payload = { query: searchQuery.value, location: searchLocation.value };
  console.log("Payload being sent:", JSON.stringify(payload, null, 2));

  try {
    const token = localStorage.getItem("authToken");
    if (!token) return console.error("Authorization token is missing!");

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

    if (
      response.data.message ===
      "Initial Search - Search results retrieved successfully."
    ) {
      if (response.data.results?.length) {
        jobIds.value = response.data.results;
        const decodedJobs = decodeBase64Results(response.data.results);

        if (jobIds.value.length === decodedJobs.length) {
          jobs.value = decodedJobs.map((job, index) => ({
            ...job,
            jobId: jobIds.value[index],
          }));
          console.log("Final Jobs Array:", jobs.value);
        } else {
          console.error("Mismatch in length between jobIds and decodedJobs");
        }

        nextPageToken.value = response.data.next_page_token || null;
        if (response.data.search_id)
          localStorage.setItem("search_id", response.data.search_id);
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

// Load more job results using the stored search ID
const loadMoreJobs = async () => {
  const searchId = localStorage.getItem("search_id");
  const token = localStorage.getItem("authToken");
  if (!searchId) return console.error("Search ID is missing or expired.");

  try {
    const response = await axios.post(
      "https://asp-final-project.onrender.com/v1/search/jobs",
      { search_id: searchId },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (response.data.message) {
      const decodedJobs = decodeBase64Results(response.data.results);
      jobs.value = [...jobs.value, ...decodedJobs]; // Append new results
      console.log(response.data.message);
    } else {
      console.log("No more results.");
    }
  } catch (error) {
    console.error("Error loading more jobs:", error);
  }
};

// Save a job to the user's favorites
const saveJob = async (jobId) => {
  const token = localStorage.getItem("authToken");

  try {
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
    const applicationId = response.data.application_id;
    if (!applicationId)
      throw new Error("No application_id found in the response");

    points.value = response.data.points.total_points;

    // Fetch saved job details
    const savedJobDetails = await axios.get(
      `https://asp-final-project.onrender.com/v1/application/details/${applicationId}`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    savedJobs.value = savedJobDetails.data;

    // Prevent duplicate entries in favorites
    if (
      !_.some(
        favouritesList.value,
        (job) => job.job.job_id === savedJobs.value.job.job_id
      )
    ) {
      favouritesList.value.push(savedJobs.value);
    } else {
      console.log("Job already exists in favorites");
    }
  } catch (error) {
    console.error("Error:", error.response?.data || error.message);
    throw error;
  }
};

// Fetch the user's current points
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

    points.value = response.data.current_points || 0;
  } catch (error) {
    console.error("Error fetching points:", error);
  }
};

// Fetch all applications for the current user
const fetchAllApplications = async () => {
  const token = localStorage.getItem("authToken");
  const userId = localStorage.getItem("user_id");
  if (!userId) return console.error("User ID not found in localStorage.");

  try {
    const response = await axios.get(
      `https://asp-final-project.onrender.com/v1/application/user/${userId}`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    console.log("Applications Fetched:", response.data);

    // Fetch details for each saved job
    for (const application of response.data) {
      await fetchJobDetails(application.application_id);
    }
    return response;
  } catch (error) {
    console.error(
      "Error fetching applications:",
      error.response?.data || error.message
    );
  }
};

// Fetch job details by application ID
const fetchJobDetails = async (applicationId) => {
  const token = localStorage.getItem("authToken");

  try {
    const savedJobDetails = await axios.get(
      `https://asp-final-project.onrender.com/v1/application/details/${applicationId}`,
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    // Prevent duplicate entries in favorites
    if (
      !_.some(
        favouritesList.value,
        (job) => job.job.job_id === savedJobDetails.data.job.job_id
      )
    ) {
      favouritesList.value.push(savedJobDetails.data);
    } else {
      console.log("Job already exists in favorites");
    }
  } catch (error) {
    console.error(
      "Error fetching job details:",
      error.response?.data || error.message
    );
  }
};

// Fetch job details using job ID
const getJobDetails = async (jobId) => {
  const token = localStorage.getItem("authToken");
  if (!token) return console.error("Authorization token is missing.");

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
  if (!token) {
    console.error("Authorization token is missing.");
    return;
  }

  try {
    console.log("Deleting job:", applicationId);

    // delete job
    const response = await axios.get(
      `https://asp-final-project.onrender.com/v1/application/delete/${applicationId}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (response.data) {
      console.log("Job deleted successfully");

      // Fetch all applications again to reflect the updated list
      const result = await fetchAllApplications();

      console.log("result.data:", result.data);

      const jobIdsInFavourites = favouritesList.value.map(
        (item) => item.job?.job_id
      );

      console.log("Job IDs in favourites:", jobIdsInFavourites);

      // Extract job_ids from result.data
      const updatedJobIds = result.data.map((app) => app?.job_id);
      console.log("Updated job IDs:", updatedJobIds);

      // Filter out jobs in favourites that don't exist in updatedJobIds
      const filteredFavourites = favouritesList.value.filter((item) =>
        updatedJobIds.includes(item.job?.job_id)
      );

      console.log("Filtered favourites list:", filteredFavourites);

      // Update the favouritesList with the filtered list
      favouritesList.value = filteredFavourites;
    }
  } catch (error) {
    console.error("Error deleting job:", error.response?.data || error.message);
  }
};

onMounted(() => {
  fetchPoints();
  // fetchLeaderboard();
  fetchAllApplications();
  console.log("favouritesList:", favouritesList);
});
</script>

<style scoped>
.job-card {
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.4);
  margin-top: 100px;
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
  background-color: #ebf3fb;
}

/* Leaderboard Card */
/* .leaderboard-card {
  width: 450px;
  max-width: 100%;
  padding: 20px;
  border-radius: 15px;
  background-color: #f8f9fa;
} */
.search-input {
  border-radius: 12px;
  padding: 10px;
  transition: 0.3s;
}
.search-input:hover {
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
}
</style>
