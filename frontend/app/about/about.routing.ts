import { ModuleWithProviders } from "@angular/core";
import { RouterModule } from "@angular/router";

import { AboutComponent } from "./about.component";

export const routing: ModuleWithProviders = RouterModule.forChild([
  { path: "about", component: AboutComponent},
]);
