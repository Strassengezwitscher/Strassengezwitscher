import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";

import { TweetComponent } from "./tweet.component";

@NgModule({
  imports: [BrowserModule],
  declarations: [TweetComponent],
  exports: [TweetComponent],
})
export class TwitterModule {}
