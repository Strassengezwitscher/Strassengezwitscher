import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { MaterialModule } from "@angular/material";

import { BlogComponent } from "./blog.component";
import { routing } from "./blog.routing";

@NgModule({
  imports: [MaterialModule, routing],
  declarations: [BlogComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class BlogModule {}
