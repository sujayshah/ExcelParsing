import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';

export interface Tile {
  color: string;
  text: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  tiles: Tile[] = [
    {text: '1', color: 'lightblue'},
    {text: '2', color: 'lightgreen'},
    {text: '3', color: 'lightpink'},
    {text: '4', color: '#DDBDF1'},
  ];
  defaultTiles = Object.assign([], this.tiles);

  constructor() {

  }
  
  addColor(color: string) {
    let newTile : Tile = {color: color, text: (this.tiles.length + 1).toString()};
    this.tiles.push(newTile);
  }

  resetDefault() {
    this.tiles = Object.assign([], this.defaultTiles);;
  }

  onSubmit(form) {
    console.log(form);
  }
}