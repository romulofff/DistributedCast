import { Component, OnInit } from '@angular/core';
import { Podcast } from '../podcast';
import { PODCASTS } from '../mock-podcasts'

@Component({
  selector: 'app-podcasts',
  templateUrl: './podcasts.component.html',
  styleUrls: ['./podcasts.component.css']
})
export class PodcastsComponent implements OnInit {

  podcasts = PODCASTS;
  selectedPodcast: Podcast;
  onSelect(podcast: Podcast): void {
    this.selectedPodcast = podcast;
  }

  constructor() { }

  ngOnInit() {
  }

}
