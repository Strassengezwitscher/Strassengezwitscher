import { NgModule } from "@angular/core";
import { MdButtonModule } from "@angular2-material/button/button";
import { MdCheckboxModule } from "@angular2-material/checkbox/checkbox";
import { MdSlideToggleModule } from "@angular2-material/slide-toggle/slide-toggle";
import { MdCardModule } from "@angular2-material/card/card";
import { MdIconModule } from "@angular2-material/icon/icon";
import { MdInputModule } from "@angular2-material/input/input";
import { MdToolbarModule } from "@angular2-material/toolbar/toolbar";
import { MdTooltipModule } from "@angular2-material/tooltip/tooltip";
import { MdSidenavModule } from "@angular2-material/sidenav/sidenav";

const MATERIAL_MODULES = [
  MdButtonModule,
  MdCardModule,
  MdCheckboxModule,
  MdIconModule,
  MdInputModule,
  MdSlideToggleModule,
  MdToolbarModule,
  MdTooltipModule,
  MdSidenavModule,
];

@NgModule({
  imports: MATERIAL_MODULES,
  exports: MATERIAL_MODULES,
})
export class MaterialModule { }
