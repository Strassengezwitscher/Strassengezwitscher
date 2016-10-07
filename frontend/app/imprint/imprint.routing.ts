import { ModuleWithProviders } from "@angular/core";
import { RouterModule } from "@angular/router";

import { ImprintComponent } from "./imprint.component";

export const routing: ModuleWithProviders = RouterModule.forChild([
  { path: "imprint", component: ImprintComponent},
]);
