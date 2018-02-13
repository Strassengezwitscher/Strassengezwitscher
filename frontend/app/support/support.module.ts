import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { MaterialModule } from "@angular/material";

import { SupportComponent } from "./support.component";
import { routing } from "./support.routing";

@NgModule({
  imports: [MaterialModule, routing],
  declarations: [SupportComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class SupportModule {}
