// Mock API service
export const fetchApplications = async () => {
    return [
      { id: 1, title: 'Software Engineer Intern', status: 'Submitted', deadline: '2025-01-20' },
      { id: 2, title: 'Data Analyst Intern', status: 'Interview Scheduled', deadline: '2025-01-25' },
      { id: 3, title: 'UX Designer Intern', status: 'Under Review', deadline: '2025-02-01' },
    ];
  };
  
  // export const fetchTasks = async () => {
  //   return [
  //     { id: 1, description: 'Apply to 3 remote jobs', completed: false },
  //     { id: 2, description: 'Save 5 job postings', completed: false },
  //     { id: 3, description: 'Follow up on 2 applications', completed: true },
  //   ];
  // };
  