Dieser Ordner enthält die Training Frameworks für die Modelle der lernbasierten Agenten.

Die Modelle nutzen die Keras Dense Layer Struktur. Es werden 2 Hidden Layer erstellt die Anzahl der Units/Neuronen ergeben sich aus dem Mittelwert der Eingabe- und Ausgabeparameter.

Die Agenten setzten sich aus vier Modellen mit nacheinander ablaufenden Aufgaben zusammen:
    - Erhöhen, Checken oder Passen beim Reizen
    - Aufnehmen des Skats
    - Auswahl des Spielmodus
    - Abwerfen von 2 Karten in den Skat

Das Training-Framework sammelt dabei die Rewards der nachfolgenden Modelle ein um für jeden Zwischenschritt den zukünftigen Wert zu schätzen.

Die einzelnen Schwierigkeitsgrade unterscheiden sich durch die in der Spielumgebung definierten Reward-Funktionen im letzten Schritt.
    - Leicht: Reward basierend auf der Anzahl der Buben
    - Medium: Reward basierend auf der Anzahl der Trümpfe bzw niedrigen Karten im Nullspiel
    - Schwer: Reward basierend auf dem Gewinnwert in einem simulierten Spiel

Die Parameter der Umgebung lassen sich im init der jeweiligen Spielumgebung anpassen (Trainingsgegner).

Die Modelle werden nach 100 Episoden im Ordner gespeichert. Überschreibt alte Modelle, ein manuelles Kopieren ist erforderlich.

Anm.: Diese Version des Frameworks erlaubt kein Laden und Trainieren existierender Modelle.