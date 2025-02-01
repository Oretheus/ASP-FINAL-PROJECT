import { createApp } from "vue";
import { Quasar } from "quasar";
import { useDialogPluginComponent } from 'quasar'
import router from './router/router.js';

// Import Quasar css
import 'quasar/src/css/index.sass'

import App from './App.vue'

createApp(App)
  .use(Quasar, {
    plugins: {}
  })
  .use(router)
  .mount("#app");
