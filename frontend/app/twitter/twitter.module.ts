import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { JsonpModule } from "@angular/http";

import { TweetComponent } from "./tweet.component";
import { TwitterService } from "./twitter.service";

@NgModule({
  imports: [BrowserModule, JsonpModule],
  declarations: [TweetComponent],
  exports: [TweetComponent],
  providers: [TwitterService],
})
export class TwitterModule {}
