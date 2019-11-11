import { Component, OnInit } from '@angular/core';

import { PodcastService } from '../podcast.service';

@Component({
  selector: 'app-podcasts',
  templateUrl: './podcasts.component.html',
  styleUrls: ['./podcasts.component.css']
})
export class PodcastsComponent implements OnInit {

  podcasts: any=[];

  constructor(private podcastService: PodcastService) { }

  getPodcasts() {
    return this.podcastService.getPodcasts()
      .subscribe(
        (content) => {
          this.podcasts = content.data
        })
  }

  fileToUpload: File = null;
  handleFileInput(files: FileList) {
    console.log(files)
    this.fileToUpload = files.item(0);
  }

  add(title: string, author: string, id: string): void {
    this.podcastService.addPodcast(title, author, id, this.fileToUpload)
      .subscribe(podcast => {
        
        this.podcasts.push(podcast);
      });
  }

  delete(id:string): void {
    this.podcastService.deletePodcast(id)
      .subscribe(podcast => {
        this.podcasts.push(podcast);
      })
  }

  ngOnInit() {
    this.getPodcasts();
  }

}