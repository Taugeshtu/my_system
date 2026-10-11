{
  description = "my_system - plain-text digital operating environment tooling";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];

      mkTools = pkgs: pkgs.runCommand "my-system-tools" {
        nativeBuildInputs = [ pkgs.bash pkgs.python3 pkgs.uv ];
      } ''
        mkdir -p $out/bin
        cp ${self}/_tools/regenerate_index.py $out/bin/regenerate_index
        cp ${self}/_tools/regenerate_work.py $out/bin/regenerate_work
        cp ${self}/_tools/chunkify_text.py $out/bin/chunkify_text
        cp ${self}/_tools/to-ingress $out/bin/to-ingress
        cp ${self}/_tools/yoink.py $out/bin/yoink
        chmod +x $out/bin/*
        patchShebangs $out/bin
      '';
    in {
      packages = nixpkgs.lib.genAttrs systems (system: {
        default = mkTools nixpkgs.legacyPackages.${system};
      });

      homeManagerModules.default = { pkgs, ... }: {
        home.packages = [
          (mkTools pkgs)
          pkgs.uv
        ];
      };
    };
}
