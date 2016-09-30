import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";

import { AboutComponent } from "./about.component";
import { routing } from "./about.routing";

@NgModule({
  imports: [routing],
  declarations: [AboutComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class AboutModule {}
