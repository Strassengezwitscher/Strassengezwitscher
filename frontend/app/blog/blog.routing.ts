import { ModuleWithProviders } from "@angular/core";
import { RouterModule } from "@angular/router";

import { BlogComponent } from "./blog.component";

export const routing: ModuleWithProviders = RouterModule.forChild([
  { path: "blog", component: BlogComponent},
]);
