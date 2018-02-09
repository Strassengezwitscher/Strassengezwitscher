import { ModuleWithProviders } from "@angular/core";
import { RouterModule } from "@angular/router";

import { DonateComponent } from "./donate.component";

export const routing: ModuleWithProviders = RouterModule.forChild([
  { path: "donate", component: DonateComponent},
]);
