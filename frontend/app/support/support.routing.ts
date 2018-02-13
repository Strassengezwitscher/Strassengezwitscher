import { ModuleWithProviders } from "@angular/core";
import { RouterModule } from "@angular/router";

import { SupportComponent } from "./support.component";

export const routing: ModuleWithProviders = RouterModule.forChild([
  { path: "support", component: SupportComponent},
]);
