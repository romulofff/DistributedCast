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

  selectedPodcast: Podcast;
  onSelect(podcast: Podcast): void {
    this.selectedPodcast = podcast;
  }

  constructor(private podcastService: PodcastService) { }

  getPodcasts(): void {
    this.podcastService.getPodcasts().subscribe(podcasts => this.podcasts = podcasts)
  }

  // getPodcasts(): void {
    // this.podcasts = this.podcastService.getPodcasts();
  // }

  ngOnInit() {
    this.getPodcasts();
  }

}
