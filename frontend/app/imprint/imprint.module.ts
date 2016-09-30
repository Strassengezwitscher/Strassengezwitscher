import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";

import { ImprintComponent } from "./imprint.component";
import { routing } from "./imprint.routing";

@NgModule({
  imports: [routing],
  declarations: [ImprintComponent],
  exports: [ImprintComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class ImprintModule {}
