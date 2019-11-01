import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Podcast } from '../podcast';
import { PodcastService } from '../podcast.service';
import { PODCASTS } from '../mock-podcasts';

@Component({
  selector: 'app-podcasts',
  templateUrl: './podcasts.component.html',
  styleUrls: ['./podcasts.component.css']
})
export class PodcastsComponent implements OnInit {

  podcasts: Podcast[];

  constructor(private podcastService: PodcastService) { }

  getPodcasts(): void {
    this.podcastService.getPodcasts()
      .subscribe(podcasts => this.podcasts = podcasts)
  }

  ngOnInit() {
    this.getPodcasts();
  }

}
