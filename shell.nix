# shell.nix
{ pkgs ? import <nixpkgs> {} }:
let
  my-python-packages = ps: with ps; [
    django
    # other python packages
  ];
  my-python = pkgs.python311.withPackages my-python-packages;
in my-python.env
